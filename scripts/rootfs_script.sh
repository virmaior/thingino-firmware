#!/bin/bash

#
# RootFS helper
#

BOOTLOADER=$(echo $BR2_PACKAGE_THINGINO_UBOOT_BOARDNAME | tr -d '"')

# Preset the hostname
IMAGE_ID=$(echo $BR2_CONFIG | awk -F '/' '{print $(NF-1)}')
HOSTNAME=ing-$(echo $IMAGE_ID | awk -F '_' '{print $1 "-" $2}')
echo "$HOSTNAME" > ${TARGET_DIR}/etc/hostname
sed -i "/^127.0.1.1/c127.0.1.1\t$HOSTNAME" ${TARGET_DIR}/etc/hosts

cd $BR2_EXTERNAL
GIT_BRANCH=$(git branch | grep ^* | awk '{print $2}')
GIT_HASH=$(git show -s --format=%H)
GIT_TIME=$(TZ=UTC0 git show --quiet --date='format-local:%Y-%m-%d %H:%M:%S +0000' --format="%cd")
BUILD_TIME="$(env -u SOURCE_DATE_EPOCH TZ=UTC date '+%Y-%m-%d %H:%M:%S %z')"
BUILD_ID="${GIT_BRANCH}+${GIT_HASH:0:7}, ${BUILD_TIME}"
COMMIT_ID="${GIT_BRANCH}+${GIT_HASH:0:7}, ${GIT_TIME}"
cd -

#
# Create the /etc/os-release file
#

# Take care of dropbear
rm ${TARGET_DIR}/etc/dropbear
mkdir -p ${TARGET_DIR}/etc/dropbear

FILE=${TARGET_DIR}/usr/lib/os-release

# Create a temporary file
tmpfile=$(mktemp)

# Prefix exiting buildroot entries
sed 's/^/BUILDROOT_/' $FILE > $tmpfile

# Add Thingino entries
echo "NAME=Thingino
ID=thingino
VERSION=\"1 (Ciao)\"
VERSION_ID=1
VERSION_CODENAME=ciao
PRETTY_NAME=\"Thingino 1 (Ciao)\"
ID_LIKE=buildroot
CPE_NAME=\"cpe:/o:thinginoproject:thingino:1\"
LOGO=thingino-logo-icon
ANSI_COLOR=\"1;34\"
HOME_URL=\"https://thingino.com/\"
ARCHITECTURE=mips
IMAGE_ID=${IMAGE_ID}
BUILD_ID=\"${BUILD_ID}\"
BUILD_TIME=\"${BUILD_TIME}\"
COMMIT_ID=\"${COMMIT_ID}\"
BOOTLOADER=$BOOTLOADER
HOSTNAME=${HOSTNAME}
TIME_STAMP=$(date +%s)" | tee $FILE

# Append the rest of the file
cat $tmpfile | tee -a $FILE

# Remove the temporary file
rm $tmpfile

#
# Create the /etc/thingino.config file
#

SYSTEM_CONFIG=${TARGET_DIR}/etc/thingino.config

touch $SYSTEM_CONFIG

# Add the common configuration
cat ${BR2_EXTERNAL}/configs/system/00_common.config | tee -a $SYSTEM_CONFIG

# Add the camera specific configuration
cat ${BR2_EXTERNAL}/configs/system/${CAMERA}.config | tee -a $SYSTEM_CONFIG

#
# Remove unnecessary files
#

if [ -f "${TARGET_DIR}/lib/libconfig.so" ]; then
	rm -vf ${TARGET_DIR}/lib/libconfig.so*
fi

if [ -f "${TARGET_DIR}/lib/libstdc++.so.6.0.33-gdb.py" ]; then
	rm -vf ${TARGET_DIR}/lib/libstdc++.so.6.0.33-gdb.py
fi

if [ -f "${TARGET_DIR}/etc/init.d/S50dropbear" ]; then
	mv ${TARGET_DIR}/etc/init.d/S50dropbear ${TARGET_DIR}/etc/init.d/S30dropbear
fi

if grep -q ^BR2_TOOLCHAIN_USES_MUSL $BR2_CONFIG; then
	ln -srf ${TARGET_DIR}/lib/libc.so ${TARGET_DIR}/lib/ld-uClibc.so.0
	ln -srf ${TARGET_DIR}/lib/libc.so ${TARGET_DIR}/usr/bin/ldd
fi

if grep -q ^BR2_PACKAGE_EXFAT_UTILS $BR2_CONFIG; then
	rm -vf ${TARGET_DIR}/usr/sbin/exfatattrib
	rm -vf ${TARGET_DIR}/usr/sbin/dumpexfat
	rm -vf ${TARGET_DIR}/usr/sbin/exfatlabel
	rm -vf ${TARGET_DIR}/etc/network/nfs_check
fi
