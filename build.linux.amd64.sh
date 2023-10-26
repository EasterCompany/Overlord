os="linux"
arch="amd64"
pkg="olt_1.3.1-1_$arch"
outdir="$(pwd)/bin/$pkg"
sudo mkdir -p bin
sudo rm -rf bin
sudo mkdir -p bin
sudo mkdir -p $outdir
sudo mkdir -p $outdir/bin
sudo mkdir -p $outdir/usr/bin
sudo mkdir -p $outdir/DEBIAN
echo "Package: olt
Version: 1.3.1
Maintainer: Easter Company <contact@easter.company>
Depends: libc6
Architecture: amd64
Homepage: https://overlord.easter.company
Description: overlord tools" > "$outdir/DEBIAN/control"
./build.sh "$(pwd)/src" "$(pwd)/bin/${pkg}/usr/bin/olt" "linux" "amd64"
dpkg --build "$outdir"
dpkg-deb --info "$outdir.deb"
dpkg-deb --contents "$outdir.deb"
