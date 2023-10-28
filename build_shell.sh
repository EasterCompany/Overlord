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
OX_ARGS="$@"

if [ $OX_OS == "linux" ]; then
  OX_BINARY="$OX_BUNDLE/usr/bin/ox"
else
  OX_BINARY="$OX_BUILD_DIR/ox"
fi

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

if test -f "$OX_BUILD_DIR"; then
  echo "  deleting pre-existing build contents..."
  sudo rm -rf $OX_BUILD_DIR
  echo " "
fi

if [ "$OX_OS" == "linux" ]; then
  if [ "$OX_ARCH" == "amd64" ]; then
    echo "> Creating new build diretories"
    sudo mkdir -p "$OX_BUILD_DIR"
    sudo mkdir -p "$OX_BUNDLE"
    sudo mkdir -p "$OX_BUNDLE/bin"
    sudo mkdir -p "$OX_BUNDLE/usr"
    sudo mkdir -p "$OX_BUNDLE/usr/bin"
    echo "  Done."
    mkdir -p "$OX_BUNDLE/DEBIAN"
    echo "  creating package control file..."
    echo "Package: ox
Version: 0.0.1
Maintainer: Easter Company <contact@easter.company>
Depends: libc6
Architecture: $OX_ARCH
Homepage: https://overlord.easter.company
Description: ox command line interface, package manager, server, and more" > "$OX_BUNDLE/DEBIAN/control"
    echo " "
    echo "> Compile binaries from source"
    GOOS="$OX_OS"
    GOARCH="$OX_ARCH"
    go build -o "$OX_BINARY" "$OX_SOURCE_DIR"
    if test -f $OX_BINARY; then
      echo "  Successfully compiled"
      echo " "
    else
      echo " "
      exit
    fi
    echo " "

    echo "> Removing Existing Symlinks"
    if test -f "/usr/bin/ox"; then
      sudo rm -rf /usr/bin/ox
      echo "  [DELETED] /usr/bin/ox"
    fi
    if test -d "/usr/lib/ox"; then
      sudo rm -rf /usr/lib/ox
      echo "  [DELETED] /usr/lib/ox"
    fi
    if test -d "/usr/local/lib/ox"; then
      sudo rm -rf /usr/local/lib/ox
      echo "  [DELETED] /usr/local/lib/ox"
    fi
    echo " "

    echo "> Remove Existing Installation"
    sudo apt remove ox -y
    echo " "

    echo "> Bundle Debian Package"
    sudo dpkg --build "$OX_BUNDLE"
    sudo dpkg-deb --info "$OX_PACKAGE"
    sudo dpkg-deb --contents "$OX_PACKAGE"
    echo " "

    echo "> Install New Package"
    sudo apt-get install -f "$OX_PACKAGE"
    echo " "
  fi
  exit
fi

if [ "$OX_OS" == "darwin" ]; then
  if [ "$OX_ARCH" == "amd64" ]; then
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
  fi
  exit
fi
