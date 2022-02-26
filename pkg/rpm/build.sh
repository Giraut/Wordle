#!/bin/sh

# Directories and files
BUILDSCRIPTPATH=$(realpath "$0")
BUILDSCRIPTDIR=$(dirname ${BUILDSCRIPTPATH})
SRC=$(realpath ${BUILDSCRIPTDIR}/../..)
VERSION=$(grep -E "^ +v[0-9]+\.[0-9]+\.[0-9]+ *$" ${SRC}/README | sed -E 's/[ v]*//')
PKGSPEC=${BUILDSCRIPTDIR}/wordle.spec
PKG=wordle-${VERSION}-0.noarch
PKGBUILD=${BUILDSCRIPTDIR}/${PKG}
BUILDROOT=${PKGBUILD}/BUILDROOT/${PKG}
RPMDIR=${PKGBUILD}/RPMS

# Create a fresh RPM build directory
rm -rf ${PKGBUILD}
mkdir -p ${PKGBUILD}/SPECS
mkdir -p ${PKGBUILD}/SOURCES
mkdir -p ${PKGBUILD}/BUILD
mkdir -p ${PKGBUILD}/BUILDROOT
mkdir -p ${PKGBUILD}/RPMS
mkdir -p ${PKGBUILD}/SRPMS

# Copy the spec file into the RPM build directory
cp -a ${PKGSPEC} ${PKGBUILD}/SPECS

# Create empty directory structure
mkdir -p ${BUILDROOT}/usr/bin
mkdir -p ${BUILDROOT}/usr/share/doc/wordle
mkdir -p ${BUILDROOT}/usr/share/games/wordle

# Populate the package build directory with the source files
install -m 644 ${SRC}/README ${BUILDROOT}/usr/share/doc/wordle
install -m 644 ${SRC}/LICENSE ${BUILDROOT}/usr/share/doc/wordle

install -m 755 ${SRC}/wordle.py ${BUILDROOT}/usr/bin/wordle
(cd ${BUILDROOT}/usr/bin && ln -s wordle sanuli)
(cd ${BUILDROOT}/usr/bin && ln -s wordle lemot)

install -m 644 ${SRC}/en_GB.langpack ${BUILDROOT}/usr/share/games/wordle
install -m 644 ${SRC}/fi_FI.langpack ${BUILDROOT}/usr/share/games/wordle
install -m 644 ${SRC}/fr_FR.langpack ${BUILDROOT}/usr/share/games/wordle

# Fixup permissions
find ${PKGBUILD} -type d -exec chmod 755 {} \;
chmod 644 ${PKGBUILD}/SPECS/wordle.spec

# Set the version in the spec file
sed -i "s/^Version:.*\$/Version: ${VERSION}/" ${PKGBUILD}/SPECS/wordle.spec

# Build the .rpm package
rpmbuild --target=noarch --define "_topdir ${PKGBUILD}" --define "_rpmdir ${RPMDIR}" -bb ${PKGBUILD}/SPECS/wordle.spec

# Retrieve the built .rpm package
cp ${RPMDIR}/noarch/${PKG}.rpm ${BUILDSCRIPTDIR}
