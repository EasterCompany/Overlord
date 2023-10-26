package main

import (
	"os"
	"fmt"
	"runtime"
	"strings"
	"strconv"
)

type __SERVER__ struct {
	host          string
	http_protocol string
	http_path     string
	http_uri      string
	ws_protocol   string
	ws_path       string
	ws_uri        string
}

var server = __SERVER__{
	host:          "localhost:8999",
	http_protocol: "http",
	http_path:     "api",
	http_uri:      "",
	ws_protocol:   "ws",
	ws_path:       "api/ws",
	ws_uri:        "",
}

func init_server() {
  server.http_uri = server.http_protocol + "://" + server.host + "/" + server.http_path
  server.ws_uri = server.ws_protocol + "://" + server.host + "/" + server.ws_path
}
