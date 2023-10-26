package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
	"strconv"
)

type LOGIN_REQUEST struct {
	Email    string `json:"email"`
	Password string `json:"password"`
}

type LOGIN_RESPONSE struct {
	Status string      `json:"status"`
	Data   interface{} `json:"data"`
}

type __SERVER__ struct {
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

type __GROUP__ struct {
	uuid    string
	name    string
	level   int
	servers []__SERVER__
}

type __USER__ struct {
	uuid          string
	display_image string
	display_name  string
	email         string
	session       string
	permissions   int
	groups        []__GROUP__
	first_name    string
	middles_names string
	last_name     string
	last_active   string
	date_joined   string
	date_of_birth string
	logged_in     bool
	is_active     bool
	exists        bool
}

var user = __USER__{
	uuid:          "",
	display_image: "",
	display_name:  "",
	email:         "",
	session:       "",
	permissions:   0,
	groups:        []__GROUP__{},
	first_name:    "",
	middles_names: "",
	last_name:     "",
	last_active:   "",
	date_joined:   "",
	date_of_birth: "",
	logged_in:     false,
	is_active:     false,
	exists:        false,
}

func login() {
	if user.email != "null" && user.uuid != "null" && user.session != "null" {
		print("User already logged in.")
		return
	}
	print("No user profile found.")

	var loginRequest LOGIN_REQUEST
	print("\nEnter your eProfile email:\r")
	fmt.Scanln(&loginRequest.Email)
	print("\nEnter Password:\r")
	fmt.Scanln(&loginRequest.Password)
	print("")

	requestBody, err := json.Marshal(loginRequest)
	handle_error(err)

	req, err := http.NewRequest("POST", "/o-core/user/login", bytes.NewReader(requestBody))
	handle_error(err)
	req.Header.Set("Content-Type", "application/json")
	login_client := http.Client{}
	resp, err := login_client.Do(req)
	handle_error(err)
	defer resp.Body.Close()

	responseBody, err := io.ReadAll(resp.Body)
	handle_error(err)

	var loginResponse LOGIN_RESPONSE
	err = json.Unmarshal(responseBody, &loginResponse)
	handle_error(err)

	if resp.StatusCode == http.StatusOK && loginResponse.Status != "OK" {
		print("Authentication Failed.")
		os.Exit(0)
	} else if resp.StatusCode != http.StatusOK {
		print("\nSorry! Something went wrong with your login attempt.")
		print("It looks like it's something wrong with the server, please try again later.")
		os.Exit(0)
	}

	user.date_joined = loginResponse.Data.(map[string]interface{})["dateJoined"].(string)
	user.date_of_birth = loginResponse.Data.(map[string]interface{})["dateOfBirth"].(string)
	user.display_image = loginResponse.Data.(map[string]interface{})["displayImage"].(string)
	user.display_name = loginResponse.Data.(map[string]interface{})["displayName"].(string)
	user.email = loginResponse.Data.(map[string]interface{})["email"].(string)
	user.first_name = loginResponse.Data.(map[string]interface{})["firstName"].(string)
	user.middles_names = loginResponse.Data.(map[string]interface{})["middleNames"].(string)
	user.last_name = loginResponse.Data.(map[string]interface{})["lastName"].(string)
	user.permissions = loginResponse.Data.(map[string]interface{})["permissions"].(int)
	user.session = loginResponse.Data.(map[string]interface{})["session"].(string)
	print("Login successful.")
	print("hello, " + user.display_name)
	print_2fa_required_warning()
	complete_2fa_login_step("Failed Connection /w Server")
	complete_2fa_login_step("Verified Connection /w Server")
	complete_2fa_login_step("Created 2FA Request")
	complete_2fa_login_step("Failed to create 2FA Request")
	complete_2fa_login_step("User Accepted Request")
	complete_2fa_login_step("Connection Successfully Authorized")
	complete_2fa_login_step("User Blocked Connection")
	complete_2fa_login_step("Request Timed Out")
}

var _2FA_LS int = 0

func complete_2fa_login_step(label string) {
	_2FA_LS++
	print("[" + strconv.Itoa(int(_2FA_LS)) + "]" + label)
}

func print_2fa_required_warning() {
	print(`
  This is a one-time 2FA login requirement.

  Open the OLT Dashboard in either:
  your web browser (https://olt.easter.company),
  android or ios application,
  pwa, or native desktop client.

  Login to your eProfile if you haven't already.

  (Click/Tap) User icon in the top-right corner.

  (Click/Tap) Settings

  (Click/Tap) 2FA Authentication

  Now, within the OLT Dashboard you should now be viewing
  the "2FA Authentication & API Access" page.

  This view displays a list of devices that have been
  approved, revoked, or pending 2FA authentication.

  Below this list is a list of 3rd party services that have been
  approved, blocked, or pending 2FA authentication.

  (Click/Tap) The corresponding device to the one you are attempting
  to authenticate now, from the 2FA devices list.

  (Click/Tap) Verify the details presented on screen are correct, and
  then Accept or Decline the 2FA authorization request.

  If the request is not accepted within 5 minutes, the request
  will automatically be declined and this interface will exit.

  If the request is manually declined, this interface will exit.

  If the request is manually blocked, this interface will exit
  and will not be able to make further requests until the user
  as un-blocked this interface from the 2FA devices list.

  If the request is accepted, the login process will continue
  automatically.

  Press [Enter] to begin.
  `)
}
