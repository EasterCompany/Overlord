package main

import "strings"

func _args(args []string) {
	execute_match_cases := func(arg string) string {
		switch arg {
		case "v":
			return version.label
		default:
			return ""
		}
	}
	for _, str := range args {
		if strings.HasPrefix(str, "-") && len(str) > 1 {
			var arg string = strings.TrimLeft(str, "-")
			var result string = execute_match_cases(arg)
			if result != "" {
				print(result)
			}
		}
	}
}
