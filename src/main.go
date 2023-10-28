package main

import (
	"os"
)

func main() {
	__init__()
	args := os.Args[1:]
	if len(args) >= 1 {
		_args(args)
		print(_cmd(args))
	} else {
		print(
			"Overlord " +
				version.label + " " +
				version.system + " " +
				version.channel,
		)
	}
}
