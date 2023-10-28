package main

import (
	"runtime"
	"strconv"
	"strings"
)

func _version(args []string) string {
	if len(args) > 0 {
		switch args[0] {
		case "help":
			return _version_help()
		case "list":
			return _version_list()
		}
	}
	return _version_error("invalid options")
}

var _version_help = func() string {
	return "command <version> help:\n"
}

var _version_list = func() string {
	return header("version") +
		"\nlabel: " + version.label +
		"\nchannel: " + version.channel +
		"\nsystem: " + version.system
}

var _version_error = func(msg string) string {
	return "command <version> error: " + msg
}

type Version struct {
	channel string
	major   int
	minor   int
	patch   int
	hotfix  int
	label   string
	system  string
}

var version = Version{
	channel: "Latest",
	major:   1,
	minor:   3,
	patch:   0,
	hotfix:  1,
	label:   "",
	system:  strings.ToUpper(string(runtime.GOOS[0])) + string(runtime.GOOS[1:]),
}

func __init__() {
	version.label =
		strconv.Itoa(int(version.major)) + "." +
			strconv.Itoa(version.minor) + "." +
			strconv.Itoa(version.patch)
	if version.hotfix > 0 {
		version.label = version.label + "-" + strconv.Itoa(version.hotfix)
	}
}
