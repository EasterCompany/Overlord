echo "$@"
echo "Building olt-$3-$4..."
GOPATH="$1" GOOS=$3 GOARCH=$4 go build -o "$2" "$1"
echo
