os="linux"
arch="amd64"
version="0.0.1"
build="0"
source="$(pwd)"
src="$source/src"
build="$source/build"
pkg="ox_$version-"$build"_$arch"
bundle="$build/$pkg"
out="$bundle/usr/bin/ox"
deb="$bundle.deb"
local_packages="$HOME/.olt-pkgs"

clear
echo "> building ox"
echo "  os: $os"
echo "  arch: $arch"
echo "  version: $version"
echo "  build: $build"
echo "  pkg: $pkg"
echo "  source: $source"
echo "  build: $build"
echo "  bundle: $bundle"
echo "  deb: $deb"

if [ ! -d "$build" ]; then
  echo "> making bin directory ($build)"
  sudo mkdir "$build"
fi

if [ -d "$bundle" ]; then
  echo "> removing previous build artifacts ($bundle)"
  sudo rm -rf $bundle
fi

if [ -d "$deb" ]; then
  echo "> removing previous build ($deb)"
  sudo rm -rf $deb
fi

echo "> create directories"
mkdir -p $bundle
mkdir -p $bundle/bin
mkdir -p $bundle/usr/bin
mkdir -p $bundle/DEBIAN

echo "> package control file"
echo "Package: ox
Version: 0.0.1
Maintainer: Easter Company <contact@easter.company>
Depends: libc6
Architecture: $arch
Homepage: https://overlord.easter.company
Description: ox command line interface, package manager, server, and more" > "$bundle/DEBIAN/control"

echo "> build binary from source"
GOPATH="$src" GOOS=$os GOARCH=$arch go build -o "$out" "$src"

echo ">  binary into deb package"
sudo dpkg --build "$bundle"
sudo dpkg-deb --info "$deb"
sudo dpkg-deb --contents "$deb"

echo "> remove existing ox installation"
sudo apt remove ox -y

echo "> remove existing bundle"
sudo rm -rf "$bundle"

echo "> install new package"
sudo apt-get install -f "$deb"

echo ">
