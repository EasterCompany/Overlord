package main

import (
	"os"
	"fmt"
	"strings"
)

func log(msg string) {
	fmt.Println(msg)
}

func error(code string, err string) {
	fmt.Println("\n[ERROR]")
	fmt.Println(err)
	fmt.Println("\nError code: OLT_CLI_ERROR_" + code)
	os.Exit(1)
}

func confirm() bool {
	var input string = ""
	fmt.Scanln(&input)
	input = strings.ToLower(input)
	if input == "y" || input == "yes" || input == "confirm" || input == "ok" || input == "agree" {
		return true
	}
	return false
}
