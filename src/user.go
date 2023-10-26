package main

type LOGIN_REQUEST struct {
	Email    string `json:"email"`
	Password string `json:"password"`
}

type LOGIN_RESPONSE struct {
	Status string      `json:"status"`
	Data   interface{} `json:"data"`
}

type __USER__ struct {
	uuid          string
	display_image string
	display_name  string
	email         string
	session       string
	permissions   float64
	first_name    string
	middles_names string
	last_name     string
	last_active   string
	date_joined   string
	date_of_birth string
}

var user = __USER__{
	uuid:          "null",
	display_image: "null",
	display_name:  "null",
	email:         "null",
	session:       "null",
	permissions:   0,
	first_name:    "null",
	middles_names: "null",
	last_name:     "null",
	last_active:   "null",
	date_joined:   "null",
	date_of_birth: "null",
}

type __ORG__ struct {
	uuid          string
	tier          string
	local_port    string
	display_image string
	display_name  string
	contact_email string
	permissions   string
}

var org = __ORG__{
	uuid:          "0",
	tier:          "Local Host",
	local_port:    "8999",
	display_image: "null",
	display_name:  user.first_name + "'s Local Network",
	contact_email: user.first_name + "@local.network",
	permissions:   "99",
}

func login() {
	if user.email != "null" && user.uuid != "null" && user.session != "null" {
		fmt.Println("User already logged in.")
	}
	fmt.Println("No user profile found.")

	var loginRequest LOGIN_REQUEST
	fmt.Println("\nEnter your eProfile email:\r")
	fmt.Scanln(&loginRequest.Email)
	fmt.Println("\nEnter Password:\r")
	fmt.Scanln(&loginRequest.Password)
	fmt.Println("")

	requestBody, err := json.Marshal(loginRequest)
	if err != nil {
		fmt.Println(err)
		return
	}

	req, err := http.NewRequest("POST", server.http_uri+"/o-core/user/login", bytes.NewReader(requestBody))
	if err != nil {
		log.Fatalln(err)
	}
	req.Header.Set("Content-Type", "application/json")
	login_client := http.Client{}
	resp, err := login_client.Do(req)
	if err != nil {
		log.Fatalln(err)
	}
	defer resp.Body.Close()

	responseBody, err := io.ReadAll(resp.Body)
	if err != nil {
		log.Fatalln(err)
	}

	var loginResponse LOGIN_RESPONSE
	err = json.Unmarshal(responseBody, &loginResponse)
	if err != nil {
		log.Fatalln(err)
	}

	if resp.StatusCode == http.StatusOK && loginResponse.Status != "OK" {
		fmt.Println("Authentication Failed.")
		os.Exit(0)
	} else if resp.StatusCode != http.StatusOK {
		fmt.Println("\nSorry! Something went wrong with your login attempt.")
		fmt.Println("It looks like it's something wrong with the server, please try again later.")
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
	user.permissions = loginResponse.Data.(map[string]interface{})["permissions"].(float64)
	user.session = loginResponse.Data.(map[string]interface{})["session"].(string)
	fmt.Println("Login successful.")
	fmt.Println("hello, " + user.display_name)
	console.print_2fa_required_warning()
	console.complete_2fa_login_step("Failed Connection /w Server")
	console.complete_2fa_login_step("Verified Connection /w Server")
	console.complete_2fa_login_step("Created 2FA Request")
	console.complete_2fa_login_step("Failed to create 2FA Request")
	console.complete_2fa_login_step("User Accepted Request")
	console.complete_2fa_login_step("Connection Successfully Authorized")
	console.complete_2fa_login_step("User Blocked Connection")
	console.complete_2fa_login_step("Request Timed Out")
}

var _2FA_LS int = 0

func complete_2fa_login_step(label string) {
	_2FA_LS++
	fmt.Println("[" + strconv.Itoa(int(_2FA_LS)) + "]" + label)
}

func print_2fa_required_warning() {
	fmt.Println(`
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
