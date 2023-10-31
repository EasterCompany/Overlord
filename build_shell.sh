OX_ARGS="$@"
OX_OS="$1"
OX_ARCH="$2"
OX_VERSION="$3"
OX_BUILD="$4"
OX_WORKING_DIR="$5"
OX_PACKAGE="ox_"$OX_VERSION"-"$OX_BUILD"_"$OX_ARCH
OX_SOURCE_DIR="$OX_WORKING_DIR/src"
OX_BUILD_DIR="$OX_WORKING_DIR/build"
OX_BUNDLE_DIR="$OX_WORKING_DIR/build/$OX_PACKAGE"
OX_DEB_FILE="$OX_BUILD_DIR/$OX_PACKAGE.deb"

if [ "$OX_OS" == "linux" ]; then
  OX_BINARY="$OX_BUNDLE_DIR/usr/bin/ox"
else
  OX_BINARY="$OX_BUILD_DIR/usr/local/bin/ox"
fi

sudo rm -rf "$OX_BUILD_DIR"
clear
echo " "
echo "> [BUILD CONFIG] "
echo "  Args: $OX_ARGS"
echo "  OS: $OX_OS"
echo "  ARCH: $OX_ARCH"
echo "  VERSION: $OX_VERSION"
echo "  BUILD: $OX_BUILD"
echo "  PACKAGE: $OX_PACKAGE"
echo "  WORKING DIR: $OX_WORKING_DIR"
echo "  SOURCE DIR: $OX_SOURCE_DIR"
echo "  BUILD DIR: $OX_BUILD_DIR"
echo "  BUNDLE DIR: $OX_BUNDLE_DIR"
echo "  BINARY: $OX_BINARY"
echo " "

if [ "$OX_OS" == "linux" ]; then
  echo "> Creating new build diretories"
  mkdir -p "$OX_BUILD_DIR"
  mkdir -p "$OX_BUNDLE_DIR/usr"
  mkdir -p "$OX_BUNDLE_DIR/usr/bin"
  mkdir -p "$OX_BUNDLE_DIR/DEBIAN"
  echo "  creating package control file..."
  echo "Package: ox
Version: 0.0.1
Maintainer: Easter Company <contact@easter.company>
Depends: libc6
Architecture: $OX_ARCH
Homepage: https://overlord.easter.company
Description: ox command line interface, package manager, server, and more" > "$OX_BUNDLE_DIR/DEBIAN/control"
  echo " "
  echo "> Compile binaries from source"
  GOOS="$OX_OS"
  GOARCH="$OX_ARCH"
  go build -o "$OX_BINARY" "$OX_SOURCE_DIR"
  if test -f $OX_BINARY; then
    echo "  Successfully compiled"
  else
    exit
  fi
  echo " "
  echo "> Remove Existing Installation"
  sudo apt remove ox -y
  echo " "
  echo "> Bundle Debian Package"
  sudo dpkg --build "$OX_BUNDLE_DIR"
  sudo dpkg-deb --info "$OX_DEB_FILE"
  sudo dpkg-deb --contents "$OX_DEB_FILE"
  echo " "
  echo "> Install New Package"
  sudo apt-get install -f "$OX_DEB_FILE"
  echo " "
fi

if [ "$OX_OS" == "darwin" ]; then
  echo "> Creating new build diretories"
  mkdir -p "$OX_BUILD_DIR"
  mkdir -p "$OX_BUNDLE_DIR/usr"
  mkdir -p "$OX_BUNDLE_DIR/usr/local/bin"
  echo " "
  echo "> Compile binaries from source"
  GOOS="$OX_OS"
  GOARCH="$OX_ARCH"
  go build -o "$OX_BINARY" "$OX_SOURCE_DIR"
  if test -f "$OX_BINARY"; then
    echo "  Successfully compiled"
    echo " "
  else
    echo " "
    exit
  fi
  if test -f "/usr/bin/ox"; then
    echo "> Removing Symlinks"
    sudo rm -rf /usr/bin/ox
    echo "  [DELETED] /usr/bin/ox"
    echo " "
  fi
  echo "> Generate Symlinks"
  sudo ln -s $OX_BUNDLE_DIR/usr/bin/ox /usr/local/bin/ox
  if test -f "/usr/bin/ox"; then
    echo "  [GENERATED] /usr/bin/ox"
  fi
  echo " "
fi

exit
