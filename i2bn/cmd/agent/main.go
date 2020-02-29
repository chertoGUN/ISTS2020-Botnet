package main

import (
	"context"
	"fmt"
	"log"
	"os"
	"time"

	"github.com/picatz/i2bn/client"
	"github.com/picatz/i2bn/server"
)

func main() {

	if len(os.Args) == 1 {
		fmt.Println("no arg given")
		os.Exit(1)
	}

	switch os.Args[1] {
	case "server":
		s := server.New()
		log.Println("Starting server")
		panic(s.ListenAndServe())
	case "client":
		for ; ; time.Sleep(3 * time.Second) {
			go func() {
				log.Println("Making client request")
				err := client.GetDemPoints(context.Background(), os.Args[2], os.Args[3], "red", "root")
				if err != nil {
					panic(err)
				}
			}()
		}
	}
}
