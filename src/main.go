package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
	"runtime"
	"strconv"
	"strings"
)

func main() {
	init_version()
	init_server()
  args := os.Args[1:]
  if len(args) > 0 {
    execute(args)
  }
}

