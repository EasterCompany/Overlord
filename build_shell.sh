OX_OS="$1"
OX_ARCH="$2"
OX_VERSION="$3"
OX_BUILD="$4"
OX_WORKING_DIR="$5"
OX_PACKAGE="ox_"$OX_VERSION"-"$OX_BUILD"_"$OX_ARCH
OX_SOURCE_DIR="$OX_WORKING_DIR/src"
OX_BUILD_DIR="$OX_WORKING_DIR/build"
OX_BUNDLE_DIR="$OX_BUILD_DIR/$PACKAGE"
OX_DEB_FILE="$OX_BUILD_DIR/$OX_PACKAGE.deb"

clear
echo " "
echo "> [BUILD CONFIG] "
echo "  OS: $OX_OS"
echo "  ARCH: $OX_ARCH"
echo "  VERSION: $OX_VERSION"
echo "  BUILD: $OX_BUILD"
echo "  PACKAGE: $OX_PACKAGE"
echo "  WORKING DIR: $OX_WORKING_DIR"
echo "  SOURCE DIR: $OX_SOURCE_DIR"
echo "  BUILD DIR: $OX_BUILD_DIR"
echo "  BUNDLE DIR: $OX_BUNDLE_DIR"
echo " "
if test -f "$OX_BUILD_DIR"; then
  echo "  deleting pre-existing build contents..."
  sudo rm -rf $OX_BUILD_DIR
  echo " "
fi

if [ "$OX_OS" == "linux" ]; then
  if [ "$OX_ARCH" == "amd64" ]; then
    $OX_GO_BINARY="$OX_BUNDLE/usr/bin/ox"
    mkdir -p "$OX_BUILD_DIR"
    mkdir -p "$OX_BUNDLE"
    mkdir -p "$OX_BUNDLE/bin"
    mkdir -p "$OX_BUNDLE/usr"
    mkdir -p "$OX_BUNDLE/usr/bin"
    mkdir -p "$OX_BUNDLE/usr/lib"
    mkdir -p "$OX_BUNDLE/usr/lib/ox"
    mkdir -p "$OX_BUNDLE/usr/lib/ox/redis"
    mkdir -p "$OX_BUNDLE/usr/lib/ox/conf"
    mkdir -p "$OX_BUNDLE/usr/lib/ox/shared"
    mkdir -p "$OX_BUNDLE/usr/local"
    mkdir -p "$OX_BUNDLE/usr/local/lib"
    mkdir -p "$OX_BUNDLE/usr/local/lib/ox/redis"
    mkdir -p "$OX_BUNDLE/usr/local/lib/ox/conf"
    mkdir -p "$OX_BUNDLE/usr/local/lib/ox/shared"
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
    GOOS="$OX_OS" GOARCH="$OX_ARCH" go build -o "$binary" "$OX_SOURCE_DIR"
    if test -f $binary; then
      echo "  Successfully compiled"
      echo " "
    else
      echo " "
      exit
    fi

    echo "> Removing existing installations"
    if test -f "/usr/bin/ox"; then
      sudo rm -rf /usr/bin/ox
      echo "  [DELETED] /usr/bin/ox"
    fi
    if test -d "/usr/lib/ox"; then
      sudo rm -rf /usr/lib/ox
      echo "  [DELETED] /usr/lib/ox"
    fi
    echo " "

    if test -d "/usr/local/lib/ox"; then
      sudo rm -rf /usr/local/lib/ox
      echo "  [DELETED] /usr/local/lib/ox"
    fi
    echo " "

    echo "> Creating symlinks"
    sudo ln -s "$binary" /usr/bin/ox
    echo "  [LINKED] /usr/bin/ox -> $binary"
    sudo ln -s "$OX_BUNDLE/usr/lib/ox" /usr/lib/ox
    echo "  [LINKED] /usr/lib/ox -> $OX_BUNDLE/usr/lib/ox"
    sudo ln -s "$OX_BUNDLE/usr/local/lib/ox" /usr/local/lib/ox
    echo "  [LINKED] /usr/local/lib/ox -> $OX_BUNDLE/usr/local/lib/ox"
    echo " "

    if [ "$6" == "pkg" ]; then
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

    if [ "$7" == "deploy" ]; then
      echo "> Deploy Package"
      echo " ..."
      echo " "
    fi

    exit
  fi
fi

if [ "$OX_OS" == "darwin" ]; then
  if [ "$OX_ARCH" == "amd64" ]; then

  fi
fi
