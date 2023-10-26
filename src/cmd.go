package main

import (
	"os"
  "fmt"
  "log"
  "runtime"
  "strings"
  "strconv"
)

func execute_cmd_line(args []string) {
	help := `
  ------------ Basic commands ------------
   help                         Show help
   exit                  Exit the program
   version                   Show version
   list                 Lists Information

   login                Connect CLI to an
                                 eProfile

   logout             Disconnect CLI from
                                 eProfile

   config                    Read & write
                           configurations

   Further documentation can be found at:
   ` + server.host + "/?a=cli-docs,help\n"
	exit := func() {
		os.Exit(0)
	}
	list := func(args []string) string {
		return strings.Join(args, "\n")
	}
	config := func() string {
		if args[0] == "config" && len(args) == 2 {
			if args[1] == "list" {
				return `list of configurations:

[` + "\033[34m" + `Version` + "\033[0m" + `]
label = ` + version_label + `
branch = ` + version.git_branch + `

[` + "\033[34m" + `eProfile` + "\033[0m" + `]
user.display_image = ` + user.display_image + `
user.display_name = ` + user.display_name + `
user.email = ` + user.email + `
user.permissions = ` + strconv.FormatFloat(user.permissions, 'f', 2, 64) + `
user.first_name = ` + user.first_name + `

[` + "\033[34m" + `Organization` + "\033[0m" + `]
org.tier = ` + org.tier + `
org.uuid = ` + org.uuid + `
org.display_image = ` + org.display_image + `
org.display_name = ` + org.display_name + `
org.contact_email = ` + org.contact_email + `
org.permissions = ` + org.permissions + `

[` + "\033[34m" + `Server` + "\033[0m" + `]
server.host = ` + server.host + `

[` + "\033[34m" + `Server` + "\033[0m" + ` http]
server.http_protocol = ` + server.http_protocol + `
server.http_path = ` + server.http_path + `
server.http_uri = ` + server.http_protocol + `://` + server.host + `/` + server.http_path + `

[` + "\033[34m" + `Server` + "\033[0m" + ` websocket]
server.ws_protocol = ` + server.ws_protocol + `
server.ws_path = ` + server.ws_path + `
server.ws_uri = ` + server.ws_protocol + `://` + server.host + `/` + server.ws_path + `
`
			}
		}
		return `
  ------------ Config ------------
  api <option> <value>
  ws <option> <value>
  version <option> <value>

  ------------ Options ------------
  list     lists all configurations

  Further documentation can be found at:
  ` + server.http_uri + "/?a=cli-docs,config\n"
	}

	switch args[0] {
	case "help":
		log(help)
	case "exit":
		exit()
	case "version":
		print(version_label)
	case "list":
		print(list(args))
	case "login":
		login()
	case "config":
		print(config())
	case "uninstall":
		uninstall()
	default:
		log("Unrecognized command: " + args[0])
	}

}
