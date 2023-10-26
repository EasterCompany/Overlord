package main

func process_cmd_line(args []string) string {
	switch args[0] {
	case "help":
		return display_help()
	case "version":
		return display_version()
	case "user":
		return display_user()
	case "servers":
		return display_servers()
	case "groups":
		return display_groups()
	case "login":
		if len(args) == 3 {
			return login(args[1], args[2])
		}
		return "Incorrect number of arguments."
	default:
		return "Unrecognized command: " + args[0]
	}
}
