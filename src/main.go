package main

import (
	"os"
)

func main() {
	__init__()
	args := os.Args[1:]
	if len(args) >= 1 {
		process_global_args_from_cmd_line(args)
		print(process_cmd_line(args))
	} else {
		print(
			"Overlord " +
				version.label + " " +
				version.system + " " +
				version.channel,
		)
	}
}
