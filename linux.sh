#!/bin/sh
rm -rf build/linux
mkdir build/linux
mkdir build/linux/modules
go build -o ./build/linux/modules/ ./modules/*.go
go build -o ./build/linux/ ./*.go
./build/linux/modules/installer "$@"
