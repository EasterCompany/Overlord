package main

func _cmd(args []string) string {
	s := args[1:]
	switch args[0] {
	case "help":
		return display_help()
	case "config":
		return _config(s)
	case "console":
		return _console(s)
	case "groups":
		return _groups(s)
	case "redis":
		return _redis(s)
	case "servers":
		return _servers(s)
	case "user":
		return _user(s)
	case "utils":
		return _utils(s)
	case "version":
		return _version(s)
	default:
		return "Unrecognized ox command: " + args[0]
	}
}
