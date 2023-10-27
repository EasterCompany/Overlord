package main

import (
	"os"
	"strings"
)

func _utils(args []string) string {
	if len(args) > 0 {
		switch args[0] {
		case "help":
			return _utils_help()
		case "list":
			return _utils_list()
		}
	}
	return _utils_error("invalid options")
}

var _utils_help = func() string {
	return "command <utils> help:\n"
}

var _utils_list = func() string {
	return "nothing to see here..."
}

var _utils_error = func(msg string) string {
	return "command <utils> error: " + msg
}

type USER_GROUP struct {
	uuid    string
	name    string
	level   int
	servers []USER_GROUP_SERVER
}

type USER_GROUP_SERVER struct {
	ssl_enabled bool
	host        string
	port        int
	uuid        string
	name        string
	label       string
	description string
	image       string
	branch      string
}

type API_TOKEN_REQUEST struct {
	Uuid    string `json:"uuid"`
	Session string `json:"session"`
}

type API_RESPONSE struct {
	Status string      `json:"status"`
	Data   interface{} `json:"data"`
}

var exit_if_not_logged_in = func() {
	if !user.logged_in {
		print(header("not logged in"))
		os.Exit(1)
	}
}

var header = func(title string) string {
	return "[" + "\033[34m" + strings.ToUpper(title) + "\033[0m" + "]"
}

var display_help = func() string {
	return ``
}
