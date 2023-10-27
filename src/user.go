package main

import "strconv"

func _user(args []string) string {
	if len(args) > 0 {
		switch args[0] {
		case "help":
			return _user_help()
		case "list":
			return _user_list()
		}
	}
	return _user_error("invalid options")
}

var _user_help = func() string {
	return "command <user> help:\n"
}

var _user_list = func() string {
	exit_if_not_logged_in()
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

var _user_error = func(msg string) string {
	return "command <user> error: " + msg
}

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

var user USER = User("root", "root")

func User(user_id string, session string) USER {
	return _User(user_id, session)
}

func _User(user_id string, session string) USER {

	account_type := "free"
	if user_id == "root" && session == "root" {
		account_type = "local"
	}

	return USER{
		Identifier: user_cache_default(user_id+".user.identifier", user_id),
		Session:    user_cache_default(user_id+".user.session", session),
		_APIToken: API_TOKEN_REQUEST{
			Uuid:    user_id,
			Session: session,
		},

		account_type: user_cache_default(user_id+".user.account_type", account_type),
		connected:    user_cache_default(user_id+".user.connected", "false") == "true",
		logged_in:    user_cache_default(user_id+".user.logged_in", "false") == "true",
		permissions:  user_cache_default(user_id+".user.permissions", "0"),
		last_active:  user_cache_default(user_id+".user.last_active", "0"),

		is_disabled:  user_cache_default(user_id+".user.is_disabled", "false") == "true",
		is_active:    user_cache_default(user_id+".user.is_active", "false") == "true",
		is_user:      user_cache_default(user_id+".user.is_user", "false") == "true",
		is_staff:     user_cache_default(user_id+".user.is_staff", "false") == "true",
		is_developer: user_cache_default(user_id+".user.is_developer", "false") == "true",
		is_admin:     user_cache_default(user_id+".user.is_admin", "false") == "true",
		is_super:     user_cache_default(user_id+".user.is_super", "false") == "true",

		groups: []USER_GROUP{},

		display_image: user_cache_default(user_id+".user.display_image", ""),
		display_name:  user_cache_default(user_id+".user.display_name", ""),
		first_name:    user_cache_default(user_id+".user.first_name", ""),
		middles_names: user_cache_default(user_id+".user.middle_names", ""),
		last_name:     user_cache_default(user_id+".user.last_name", ""),
		date_joined:   user_cache_default(user_id+".user.date_joined", ""),
		date_of_birth: user_cache_default(user_id+".user.date_of_birth", ""),

		addresses:       user_cache_default(user_id+".user.addresses", ""),
		billing_address: user_cache_default(user_id+".user.billing_address", ""),

		email:             user_cache_default(user_id+".user.email", ""),
		other_emails:      user_cache_default(user_id+".user.other_emails", ""),
		unverified_emails: user_cache_default(user_id+".user.unverified_emails", ""),
		sms:               user_cache_default(user_id+".user.sms", ""),
		other_sms:         user_cache_default(user_id+".user.other_sms", ""),
		unverified_sms:    user_cache_default(user_id+".user.unverified_sms", ""),

		_2FA_method:             user_cache_default(user_id+".user._2FA_method", "none"),
		_2FA_secret:             user_cache_default(user_id+".user._2FA_secret", ""),
		_OTA_preference:         user_cache_default(user_id+".user._OTA_preference", "none"),
		_CONTACT_preference:     user_cache_default(user_id+".user._CONTACT_preference", "none"),
		_ADVERTISING_preference: user_cache_default(user_id+".user._ADVERTISING_preference", "none"),
	}
}
