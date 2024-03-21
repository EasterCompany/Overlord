package main

import (
	"fmt"
	"os"
	"strings"

	"github.com/EasterCompany/sh"
)

var (
	DEBUG      bool   = false
	EXECUTABLE string = sh.ParseExecutable()
)

func main() {
	if strings.HasPrefix(EXECUTABLE, "/tmp/go-build") {
		DEBUG = true
	}
	if len(os.Args) >= 2 {
		executeCmdLine()
	} else {
		enterFocusMode()
	}
}

func enterFocusMode() {
	sh.Run("clear")
	displayBanner()
	for {
		awaitInput()
	}
}

func executeCmdLine() {
	// Parse user input from the command line
	target := sh.ParseTarget()
	globals := sh.ParseGlobals()
	flags := sh.ParseFlags()
	options := sh.ParseOptions()
	// Log user input when in debug mode
	if DEBUG {
		fmt.Println("TARGET:", target)
		fmt.Println("GLOBALS:", globals)
		fmt.Println("FLAGS:", flags)
		fmt.Println("OPTIONS:", options)
		fmt.Println("FULL:", os.Args)
	}
}

func displayBanner() {}

func awaitInput() {}
