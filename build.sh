# [SYSTEM] GENERAL
os="linux"
arch="amd64"
version="0.0.1"
build="0"
package="ox_"$version"-"$build"_"$arch
project_dir="$(pwd)"
src_dir="$project_dir/src"
build_dir="$project_dir/build"
rm -rf $build_dir

clear
echo " "
echo "> [CONFIG] System Settings"
echo "  os: $os"
echo "  arch: $arch"
echo "  version: $version"
echo "  build: $build"
echo "  package: $package"
echo "  project_dir: $project_dir"
echo "  src_dir: $src_dir"
echo "  build_dir: $build_dir"
echo "  loading profile '$os $arch'..."
echo " "

# [CONFIG] LINUX AMD64
bundle="$build_dir/$package"
package="$build_dir/$package.deb"
binary="$bundle/usr/bin/ox"
mkdir -p "$build_dir"
mkdir -p "$bundle"
mkdir -p "$bundle/bin"
mkdir -p "$bundle/usr/bin"
mkdir -p "$bundle/DEBIAN"

echo "> [CONFIG] Build Options"
echo "  bundle: $bundle"
echo "  package: $package"
echo "  binary: $binary"
echo "  creating package control file..."
echo "Package: ox
Version: 0.0.1
Maintainer: Easter Company <contact@easter.company>
Depends: libc6
Architecture: $arch
Homepage: https://overlord.easter.company
Description: ox command line interface, package manager, server, and more" > "$bundle/DEBIAN/control"
echo " "

echo "> Compiling"
GOOS="$os" GOARCH="$arch" go build -o "$binary" "$src_dir"
if test -f $binary; then
  echo "  Successfully compiled"
  echo " "
else
  echo " "
  exit
fi

echo "> Bundle Debian Package"
sudo dpkg --build "$bundle"
sudo dpkg-deb --info "$deb"
sudo dpkg-deb --contents "$deb"
echo " "

echo "> Remove Existing Installation"
sudo apt remove ox -y
echo " "

echo "> Install New Package"
sudo apt-get install -f "$deb"
echo " "
