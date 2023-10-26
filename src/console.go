package main

import (
	"fmt"
	"strings"
)

func print(msg string) {
	fmt.Println(msg)
}

func warn(msg string) {
	fmt.Println("WARN: " + msg)
}

func handle_error(err error) bool {
	if err != nil {
		fmt.Println("\nERROR: " + err.Error())
		return true
	}
	return false
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
