# i2bn

Botnet competition implementation for ISTS 2020

## Start Client

```console
$ go run ./cmd/agent/main.go
2020/02/29 01:49:59 Making client request
2020/02/29 01:49:59 requesting command from c2
2020/02/29 01:49:59 running command from c2 cmd="echo ggahgyvextpblhtdvamkgnpgexihtt"
2020/02/29 01:49:59 /bin/sh -c echo ggahgyvextpblhtdvamkgnpgexihtt
2020/02/29 01:49:59 cmd="echo ggahgyvextpblhtdvamkgnpgexihtt" result="ggahgyvextpblhtdvamkgnpgexihtt\n"
2020/02/29 01:49:59 posting results c2
2020/02/29 01:49:59 successfully posted to c2
...
```
