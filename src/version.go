package main

import (
	"runtime"
	"strings"
	"strconv"
)

type __VERSION__ struct {
	channel    	string
	system     	string
	major      	int64
	minor      	int64
	patch      	int64
	hotfix     	 int64
	build 			string
	label       string
}

var version = __VERSION__ {
	channel:    "local",
	system:     strings.ToUpper(string(runtime.GOOS[0])) + string(runtime.GOOS[1:]),
	major:      1,
	minor:      3,
	patch:      0,
	hotfix:			 0,
	build:			"",
	label:			"",
}

func init_version() {
	if version.channel != "Latest" && version.channel != "LTS" && version.channel != "Local" {
		error("0A", "Invalid version channel '" + version.channel + "'")
	}
	if version.system != "Linux" && version.system != "Windows" && version.system != "Darwin" {
		error("0B", "Invalid operating system '" + version.system + "'")
	}
	if version.major < 0 || version.minor < 0 || version.patch < 0 {
		error("0C", "Invalid version number")
	}
	version.build =
		strconv.Itoa(version.major * 100) +
		strconv.Itoa(version.minor * 100) +
		strconv.Itoa(version.patch)
	version.label =
		strconv.Itoa(int(version.major)) + "." +
		strconv.Itoa(version.minor) + "." +
		strconv.Itoa(version.patch) + " " +
		version.build + " " +
		version.channel + " " +
		version.system
}
