package main;

import (
	"os"
)

func main() {
	var bin string = "/bin/olt"
	var tmp string = "/tmp/olt"
	var usr_bin string = "/usr/bin/olt"
	os.RemoveAll(bin)
	os.RemoveAll(tmp)
	os.RemoveAll(usr_bin)
	os.Exit(0)
}
