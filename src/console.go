package main

import (
	"fmt"
	"strings"
)

func _console(args []string) string {
	if len(args) > 0 {
		switch args[0] {
		case "help":
			return _console_help()
		case "list":
			return _console_list()
		}
	}
	return _console_error("invalid options")
}

func log(msg string) string {
	fmt.Println(msg)
	return msg
}

var __warnings__ []string = []string{}

func logWarning(process string, msg string) string {
	var _new_warning_ string = "WARN: (" + process + ") " + msg
	__warnings__ = append(__warnings__, _new_warning_)
	return log(_new_warning_)
}

var __errors__ []string = []string{}

func logError(process string, msg string) string {
	var _new_error_ string = "ERROR: (" + process + ") " + msg
	__errors__ = append(__errors__, _new_error_)
	return log(_new_error_)
}

func logInput() string {
	i := ""
	fmt.Scanln(&i)
	return i
}

func logConfirmationInput() bool {
	i := strings.ToLower(logInput())
	if i == "y" || i == "yes" || i == "confirm" || i == "ok" || i == "agree" {
		return true
	}
	return false
}

var _console_help = func() string {
	return "command <console> help:\n"
}

var _console_list = func() string {
	return "nothing to see here..."
}

var _console_error = func(msg string) string {
	return "command <console> error: " + msg
}
