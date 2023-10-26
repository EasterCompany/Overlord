package main

import (
	"runtime"
	"strconv"
	"strings"
)

type __VERSION__ struct {
	channel string
	branch  string
	system  string
	major   int
	minor   int
	patch   int
	hotfix  int
	build   string
	label   string
}

var version = __VERSION__{
	channel: "alpha",
	branch:  "",
	major:   1,
	minor:   3,
	patch:   0,
	hotfix:  0,
	build:   "",
	label:   "",
	system:  strings.ToUpper(string(runtime.GOOS[0])) + string(runtime.GOOS[1:]),
}

func __init__() {
	version.branch = strconv.Itoa(version.major) + "." + strconv.Itoa(version.minor) + "-" + version.channel
	version.build =
		strconv.Itoa(version.major*100) +
			strconv.Itoa(version.minor*100) +
			strconv.Itoa(version.patch)
	version.label =
		strconv.Itoa(int(version.major)) + "." +
			strconv.Itoa(version.minor) + "." +
			strconv.Itoa(version.patch) + " " +
			version.build + " " +
			version.channel + " " +
			version.system
}
