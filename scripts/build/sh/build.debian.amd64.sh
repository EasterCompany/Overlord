#!/bin/sh
GOOS=linux GOARCH=amd64 go build -o bin/olt-sw-debian-amd64 olt.sw.go
GOOS=linux GOARCH=amd64 go build -o bin/olt-debian-amd64 olt.go
