package main

var user USER = User("local", "local")

func User(user_id string, session string) USER {
	return USER{
		Identifier: user_cache_default(user_id+".user.identifier", user_id),
		Session:    user_cache_default(user_id+".user.session", session),
		_APIToken: API_TOKEN_REQUEST{
			Uuid:    user_id,
			Session: session,
		},

		connected:   user_cache_default(user_id+".user.connected", "false") == "true",
		logged_in:   user_cache_default(user_id+".user.logged_in", "false") == "true",
		permissions: user_cache_default(user_id+".user.permissions", "0"),
		last_active: user_cache_default(user_id+".user.last_active", "0"),

		is_disabled:  user_cache_default(user_id+".user.is_disabled", "true") == "true",
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
