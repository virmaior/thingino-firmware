LIGHTNVR_SITE_METHOD = git
LIGHTNVR_SITE = https://github.com/opensensor/lightNVR
LIGHTNVR_SITE_BRANCH = main
LIGHTNVR_VERSION = $(shell git ls-remote $(LIGHTNVR_SITE) $(LIGHTNVR_SITE_BRANCH) | head -1 | cut -f1)

LIGHTNVR_LICENSE = MIT
LIGHTNVR_LICENSE_FILES = COPYING

LIGHTNVR_INSTALL_STAGING = YES

LIGHTNVR_DEPENDENCIES = thingino-ffmpeg thingino-libcurl sqlite

# Main application files installation
define LIGHTNVR_INSTALL_APP_FILES
	$(INSTALL) -d $(TARGET_DIR)/var/nvr
	cp -r $(@D)/web $(TARGET_DIR)/var/nvr/
	$(INSTALL) -m 755 -d $(TARGET_DIR)/etc/lightnvr
	$(INSTALL) -m 644 $(@D)/config/lightnvr.ini $(TARGET_DIR)/etc/lightnvr/lightnvr.ini
	$(INSTALL) -D -m 0755 $(@D)/lightnvr $(TARGET_DIR)/usr/bin/lightnvr
	$(INSTALL) -m 0755 -D $(LIGHTNVR_PKGDIR)/files/S95lightnvr $(TARGET_DIR)/etc/init.d/S95lightnvr
endef

# libsod libraries installation
define LIGHTNVR_INSTALL_LIBSOD
	$(INSTALL) -m 0755 -d $(TARGET_DIR)/usr/lib
	$(INSTALL) -m 0755 $(@D)/src/sod/libsod.so.1.1.9 $(TARGET_DIR)/usr/lib/
	$(INSTALL) -m 0755 -D $(@D)/src/sod/libsod.so.1 $(TARGET_DIR)/usr/lib/
	$(INSTALL) -m 0755 -D $(@D)/src/sod/libsod.so $(TARGET_DIR)/usr/lib/
endef

define LIGHTNVR_INSTALL_TARGET_CMDS
	$(LIGHTNVR_INSTALL_APP_FILES)
	$(LIGHTNVR_INSTALL_LIBSOD)
endef
$(eval $(cmake-package))
