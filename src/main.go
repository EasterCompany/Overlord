package main

import "os"

func main() {
	__init__()
	args := os.Args[1:]
	if len(args) == 0 {
		print("Overlord " + version.label)
	} else {
		print(process_cmd_line(args))
	}
}
