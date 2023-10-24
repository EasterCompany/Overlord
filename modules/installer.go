package installer

import (
	"os"
)

var tmp_app_dir string = "/tmp/olt-cli"

func clean_up_temporary_files() {
	os.RemoveAll("/tmp/olt-cli")
	os.MkdirTemp("/tmp/olt-cli", "*")
}

func clean_up_and_exit(code int) {
	clean_up_temporary_files()
	os.Exit(code)
}

func main() {
	clean_up_temporary_files()
	os.Exit(0)
}
