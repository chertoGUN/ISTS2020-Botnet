package server

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"strings"
	"time"

	"github.com/picatz/i2bn/callback"
)

func anyEmpty(strs ...string) bool {
	for _, str := range strs {
		if str == "" || strings.TrimSpace(str) == "" {
			return true
		}
	}
	return false
}

func jsonError(mesg string) []byte {
	b, err := json.Marshal(map[string]string{
		"error": mesg,
	})
	if err != nil {
		log.Println(err)
		return []byte(`{"error":null}`)
	}
	return b
}

func New() *http.Server {
	m := http.NewServeMux()

	m.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		w.Write([]byte("i2bn\n"))
	})

	m.HandleFunc("/callback", func(w http.ResponseWriter, r *http.Request) {
		switch r.Method {
		case "PUT":
			log.Printf("method=\"PUT\" url=%q", r.URL.String())
			cbreq := &callback.CommandRequest{}

			d := json.NewDecoder(r.Body)
			d.DisallowUnknownFields()
			d.Decode(cbreq)

			// verify
			// TODO: check IP
			if anyEmpty(cbreq.IP, cbreq.Team, cbreq.User) {
				http.Error(w, string(jsonError("ip, team, or user keys missing")), http.StatusBadRequest)
				return
			}

			log.Printf("team=%q ip=%q user=%q", cbreq.Team, cbreq.IP, cbreq.User)

			// generate json
			cr := callback.Response{
				Command: "echo ggahgyvextpblhtdvamkgnpgexihtt",
				ID:      "9607189a-0163-48a0-80de-99b4fa9a8155",
				IP:      "192.168.177.195",
				Team:    "5",
				Type:    "linux",
				User:    "www-data",
			}

			b, err := json.MarshalIndent(cr, "", "  ")

			if err != nil {
				// TODO: handle error
				return
			}

			w.Header().Add("Content-Type", "application/json")
			w.Header().Add("Content-Length", fmt.Sprintf("%v", len(b)))

			_, err = w.Write(b)
			if err != nil {
				// TODO: handle error
				return
			}
		case "POST":
			log.Printf("method=\"POST\" url=%q", r.URL.String())
		default:
			http.Error(w, "bad method", http.StatusBadRequest)
		}

	})

	return &http.Server{
		Handler:      m,
		Addr:         "127.0.0.1:8080",
		ReadTimeout:  15 * time.Second,
		WriteTimeout: 15 * time.Second,
		IdleTimeout:  15 * time.Second,
	}
}
