package main

func _config(args []string) string {
	if len(args) > 0 {
		switch args[0] {
		case "help":
			return _config_help()
		case "list":
			return _config_list()
		}
	}
	return _config_error("invalid options")
}

var _config_help = func() string {
	return "command <config> help:\n"
}

var _config_list = func() string {
	return "nothing to see here..."
}

var _config_error = func(msg string) string {
	return "command <config> error: " + msg
}
