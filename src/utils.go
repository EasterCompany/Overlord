package main

import (
	"strconv"
	"strings"
)

var header = func(title string) string {
	return "[" + "\033[34m" + strings.ToUpper(title) + "\033[0m" + "]"
}

var display_help = func() string {
	return ``
}

var display_version = func() string {
	return header("version") +
		"\nlabel: " + version.label +
		"\nbranch: " + version.branch
}

var display_user = func() string {
	return header("user") +
		"\nuuid: " + user.uuid +
		"\nemail: " + user.email +
		"\npermissions: " + strconv.Itoa(user.permissions) +
		"\ndisplay name: " + user.display_name +
		"\nfirst name: " + user.first_name +
		"\nmiddles names: " + user.middles_names +
		"\nlast names: " + user.last_name +
		"\nlast active: " + user.last_active +
		"\ndate joined: " + user.date_joined +
		"\ndate of birth: " + user.date_of_birth +
		"\nimage: " + user.display_image +
		"\ngroups: " + strconv.Itoa(len(user.groups)) +
		"\nservers: " + strconv.Itoa(len(user.groups))
}

var display_servers = func() string {
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
	return r
}

var display_groups = func() string {
	r := ""
	for group := range user.groups {
		r += header(user.groups[group].name) +
			"\nuuid = " + user.groups[group].uuid +
			"\nlevel = " + strconv.Itoa(user.groups[group].level) +
			"\nservers = " + strconv.Itoa(len(user.groups[group].servers))
	}
	return r
}
