#!/bin/sh

# Directories and files
BUILDSCRIPTPATH=$(realpath "$0")
BUILDSCRIPTDIR=$(dirname ${BUILDSCRIPTPATH})
SRC=$(realpath ${BUILDSCRIPTDIR}/../..)
PKGSRC=${BUILDSCRIPTDIR}/wordle
VERSION=$(grep -E "^ +v[0-9]+\.[0-9]+\.[0-9]+ *$" ${SRC}/README | sed -E 's/[ v]*//')
PKGBUILD=${PKGSRC}-${VERSION}-0_all
PKG=${PKGBUILD}.deb

# Create a fresh skeleton package build directory
rm -rf ${PKGBUILD}
cp -a ${PKGSRC} ${PKGBUILD}

# Create empty directory structure
mkdir -p ${PKGBUILD}/usr/local/bin
mkdir -p ${PKGBUILD}//usr/local/games/wordle

# Populate the package build directory with the source files
install -m 644 ${SRC}/README ${PKGBUILD}/usr/share/doc/wordle
install -m 644 ${SRC}/LICENSE ${PKGBUILD}/usr/share/doc/wordle

install -m 755 ${SRC}/wordle.py ${PKGBUILD}/usr/local/bin/wordle
(cd ${PKGBUILD}/usr/local/bin && ln -s wordle sanuli)

install -m 644 ${SRC}/en_GB.langpack ${PKGBUILD}/usr/local/games/wordle
install -m 644 ${SRC}/fi_FI.langpack ${PKGBUILD}/usr/local/games/wordle

# Set the version in the control file
sed -i "s/^Version:.*\$/Version: ${VERSION}/" ${PKGBUILD}/DEBIAN/control

# Fixup permissions
find ${PKGBUILD} -type d -exec chmod 755 {} \;
chmod 644 ${PKGBUILD}/DEBIAN/control
chmod 644 ${PKGBUILD}/usr/share/doc/wordle/copyright

# Build the .deb package
fakeroot dpkg -b ${PKGBUILD} ${PKG}
