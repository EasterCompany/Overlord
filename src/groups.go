package main

import "strconv"

func _groups(args []string) string {
	if len(args) > 0 {
		switch args[0] {
		case "help":
			return _groups_help()
		case "list":
			return _groups_list()
		}
	}
	return _groups_error("invalid options")
}

var _groups_help = func() string {
	return "command <groups> help:\n"
}

var _groups_list = func() string {
	exit_if_not_logged_in()
	if len(user.groups) == 0 {
		return header("no groups")
	}
	r := ""
	for group := range user.groups {
		r += header(user.groups[group].name) +
			"\nuuid = " + user.groups[group].uuid +
			"\nlevel = " + strconv.Itoa(user.groups[group].level) +
			"\nservers = " + strconv.Itoa(len(user.groups[group].servers))
	}
	return r
}

var _groups_error = func(msg string) string {
	return "command <groups> error: " + msg
}
