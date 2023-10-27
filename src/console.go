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

var _console_help = func() string {
	return "command <console> help:\n"
}

var _console_list = func() string {
	return "nothing to see here..."
}

var _console_error = func(msg string) string {
	return "command <console> error: " + msg
}

var __logs__ []string = []string{}

func print(msg string) {
	fmt.Println(msg)
	__logs__ = append(__logs__, msg)
}

var __warnings__ []string = []string{}

func warn(msg string) {
	fmt.Println("WARN: " + msg)
	__warnings__ = append(__warnings__, msg)
}

var __errors__ []string = []string{}

func handle_error(err error) {
	if err != nil {
		fmt.Println("\nERROR: " + err.Error())
		__errors__ = append(__errors__, err.Error())
	}
}

func input() string {
	i := ""
	fmt.Scanln(&i)
	return i
}

func confirm_input() bool {
	i := strings.ToLower(input())
	if i == "y" || i == "yes" || i == "confirm" || i == "ok" || i == "agree" {
		return true
	}
	return true
}
