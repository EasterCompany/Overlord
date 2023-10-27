package main

import (
	"strconv"
	"strings"
)

type USER struct {
	Identifier string
	Session    string
	_APIToken  API_TOKEN_REQUEST

	connected    bool
	logged_in    bool
	permissions  string
	last_active  string
	account_type string

	is_disabled  bool
	is_active    bool
	is_user      bool
	is_staff     bool
	is_developer bool
	is_admin     bool
	is_super     bool

	groups []USER_GROUP

	display_image string
	display_name  string
	first_name    string
	middles_names string
	last_name     string
	date_joined   string
	date_of_birth string

	addresses       string
	billing_address string

	email             string
	other_emails      string
	unverified_emails string
	sms               string
	other_sms         string
	unverified_sms    string

	_2FA_method             string
	_2FA_secret             string
	_OTA_preference         string
	_CONTACT_preference     string
	_ADVERTISING_preference string
}

type USER_GROUP struct {
	uuid    string
	name    string
	level   int
	servers []USER_GROUP_SERVER
}

type USER_GROUP_SERVER struct {
	ssl_enabled bool
	host        string
	port        int
	uuid        string
	name        string
	label       string
	description string
	image       string
	branch      string
}

type API_TOKEN_REQUEST struct {
	Uuid    string `json:"uuid"`
	Session string `json:"session"`
}

type API_RESPONSE struct {
	Status string      `json:"status"`
	Data   interface{} `json:"data"`
}

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
		"\nuuid: " + user.Identifier +
		"\nemail: " + user.email +
		"\npermissions: " + user.permissions +
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
