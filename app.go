package main;

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"runtime"
	"strconv"
	"strings"
)

type __VERSION__ struct {
	channel    string
	system     string
	major      int64
	minor      int64
	patch      int64
	major_lock bool
	minor_lock bool
	patch_lock bool
	git_branch string
}

var version = __VERSION__{
	channel:    "Local",
	system:     strings.ToUpper(string(runtime.GOOS[0])) + string(runtime.GOOS[1:]),
	major:      0,
	minor:      0,
	patch:      0,
	major_lock: false,
	minor_lock: false,
	patch_lock: false,
	git_branch: "Lab",
}

type __SERVER__ struct {
	host          string
	http_protocol string
	http_path     string
	http_uri      string
	ws_protocol   string
	ws_path       string
	ws_uri        string
}

var server = __SERVER__{
	host:          "localhost:8999",
	http_protocol: "http",
	http_path:     "api",
	http_uri:      "",
	ws_protocol:   "ws",
	ws_path:       "api/ws",
	ws_uri:        "",
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

type LOGIN_REQUEST struct {
	Email    string `json:"email"`
	Password string `json:"password"`
}

type LOGIN_RESPONSE struct {
	Status string      `json:"status"`
	Data   interface{} `json:"data"`
}

func execute(args []string) {
	if len(args) == 0 {
		return
	}
	cursor := "\033[34m" + user.first_name + "@" + version.git_branch + "$\033[0m " + strings.Join(args, " ")
	print := func(msg string) {
		fmt.Println(cursor + "\n" + msg + "\033[0m")
	}
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
	version_label := strconv.Itoa(int(version.major)) +
		"." + strconv.Itoa(int(version.minor)) +
		"." + strconv.Itoa(int(version.patch)) +
		" " + version.system
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
		print(help)
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
		print("Unrecognized command: " + args[0])
	}

}

func cliError(code string, err string) {
	fmt.Println("\n[ERROR]")
	fmt.Println(err)
	fmt.Println("\nError code: OLT_CLI_ERROR_" + code)
	os.Exit(1)
}

func verifyVersion() {
	if version.channel != "Latest" && version.channel != "LTS" && version.channel != "Local" {
		cliError("0A", "Invalid version channel '"+version.channel+"'")
	}
	if version.system != "Linux" && version.system != "Windows" && version.system != "Darwin" {
		cliError("0B", "Invalid operating system '"+version.system+"'")
	}
	if version.major < 0 || version.minor < 0 || version.patch < 0 {
		cliError("0C", "Invalid version number")
	}
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
	fmt.Println("[" + strconv.Itoa(int(_2FA_LS)) + "]" + label)
}

func getUserConfirmation() bool {
	var input string = ""
	fmt.Scanln(&input)
	input = strings.ToLower(input)
	if input == "y" || input == "yes" || input == "confirm" || input == "ok" || input == "agree" {
		return true
	}
	return false
}

func main() {
	verifyVersion()
	args := os.Args[1:]
	if len(args) > 0 {
		execute(args)
	}
}

func uninstall() {
	uninstall_path := func(path string) {
		fmt.Println("Removing " + path + "...")
		err := os.RemoveAll(path)
		if err != nil {
			log.Fatal(err)
		}
	}
	uninstall_path("/tmp/olt-cli")
	uninstall_path("/bin/olt-cli")
	uninstall_path("/usr/bin/olt-cli")
	uninstall_path("/usr/local/bin/olt-cli")
}
