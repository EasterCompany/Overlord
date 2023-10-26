echo "$@"
echo "building binaries..."
GOPATH="$1" GOOS=$3 GOARCH=$4 go build -o "$2" "$1"
