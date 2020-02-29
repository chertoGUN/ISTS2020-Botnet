package main

import (
	"context"
	"fmt"
	"log"
	"net"
	"os"
	"strings"
	"time"

	"github.com/picatz/i2bn/client"
)

func defaultInterface() string {
	ifaces, err := net.Interfaces()
	if err != nil {
		log.Fatal(err)
	}
	for _, iface := range ifaces {
		// must have mac address, FlagUp and FlagBroadcast
		if iface.HardwareAddr != nil && iface.Flags&net.FlagUp != 0 && iface.Flags&net.FlagBroadcast != 0 {
			addrs, err := iface.Addrs()
			if err != nil {
				continue
			}
			for _, addr := range addrs {
				return addr.String()
			}
			break
		}
	}
	return "127.0.0.1"
}

func main() {
	// ip to score
	var ip string

	if len(os.Args) == 1 {
		ip = defaultInterface()
	} else {
		ip = os.Args[1]
	}

	for ; ; time.Sleep(3 * time.Second) {
		go func() {
			log.Println("Making client request!!")
			// c2 ip + url
			c2IP := "172.16.0.56"
			c2URL := fmt.Sprintf("http://%v:80/callback", c2IP)
			// get them points
			log.Printf("trying to score %v with %v", strings.Split(ip, "/")[0], c2URL)
			err := client.GetDemPoints(context.Background(), c2URL, ip, "red", "root")
			if err != nil {
				panic(err)
			}
		}()
	}
}
