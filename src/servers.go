package main

import "strconv"

func _servers(args []string) string {
	if len(args) > 0 {
		switch args[0] {
		case "help":
			return _servers_help()
		case "list":
			return _servers_list()
		}
	}
	return _servers_error("invalid options")
}

var _servers_help = func() string {
	return "command <server> help:\n"
}

var _servers_list = func() string {
	exit_if_not_logged_in()
	r := ""
	for group := range user.groups {
		r := header(user.groups[group].name + "(" + strconv.Itoa(user.groups[group].level) + ")")
		for server := range user.groups[group].servers {
			r += "\nbranch: " + user.groups[group].servers[server].branch +
				"\nssl: " + strconv.FormatBool(user.groups[group].servers[server].ssl_enabled) +
				"\nhost: " + user.groups[group].servers[server].host +
				"\nport: " + strconv.Itoa(user.groups[group].servers[server].port) +
				"\nuuid: " + user.groups[group].servers[server].uuid +
				"\nname: " + user.groups[group].servers[server].name +
				"\nlabel: " + user.groups[group].servers[server].label +
				"\nimage: " + user.groups[group].servers[server].image +
				"\ndescription: " + user.groups[group].servers[server].description
		}
	}
	if r == "" {
		return header("no servers")
	}
	return r
}

var _servers_error = func(msg string) string {
	return "command <server> error: " + msg
}
