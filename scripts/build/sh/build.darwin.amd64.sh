#!/bin/sh
GOOS=darwin GOARCH=amd64 go build -o bin/olt-sw-darwin-amd64 olt.sw.go
GOOS=darwin GOARCH=amd64 go build -o bin/olt-darwin-amd64 olt.go
