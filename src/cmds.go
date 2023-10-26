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
	default:
		return "Unrecognized command: " + args[0]
	}
}
