package main

import (
	"os"
	"strings"
)

func main() {
	__init__()

	if len(os.Args) <= 1 {
		print("Overlord " + version.label + " " + version.system + " " + version.channel)
		os.Exit(0)
	}

	_cmd_line := _filter_cmd_line_args(os.Args[1:])
	_process_cmd_line_input(_cmd_line)
}

func _filter_cmd_line_args(args []string) []string {

	execute_write_argument_match_cases := func(arg string) {
		switch arg {
		default:
			print("Invalid write argument: " + arg)
			os.Exit(0)
		}
	}

	execute_read_argument_match_cases := func(arg string) {
		switch arg {
		case "v":
			print(version.label)
		default:
			print("Invalid read argument: " + arg)
			os.Exit(0)
		}
	}

	for _, str := range args {
		if len(str) > 1 && strings.HasPrefix(str, `.`) {
			execute_write_argument_match_cases(strings.TrimLeft(str, `.`))
		} else if len(str) > 0 && strings.HasPrefix(str, `-`) {
			execute_read_argument_match_cases(strings.TrimLeft(str, `-`))
		} else {
			break
		}
	}

	return args
}

func _process_cmd_line_input(args []string) {
	s := args[1:]
	switch args[0] {
	case "help":
		display_help()
	case "config":
		_config(s)
	case "console":
		_console(s)
	case "groups":
		_groups(s)
	case "redis":
		_redis(s)
	case "servers":
		_servers(s)
	case "user":
		_user(s)
	case "utils":
		_utils(s)
	case "version":
		_version(s)
	default:
		print("Invalid command: " + args[0])
	}
	os.Exit(0)
}
