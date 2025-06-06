# libschrift.mk
LIBSCHRIFT_SITE_METHOD = git
LIBSCHRIFT_SITE = https://github.com/tomolt/libschrift
LIBSCHRIFT_SITE_BRANCH = master
LIBSCHRIFT_VERSION = 24737d2922b23df4a5692014f5ba03da0c296112
# $(shell git ls-remote $(LIBSCHRIFT_SITE) $(LIBSCHRIFT_SITE_BRANCH) | head -1 | cut -f1)

LIBSCHRIFT_INSTALL_STAGING = YES
LIBSCHRIFT_INSTALL_TARGET = YES

define LIBSCHRIFT_BUILD_CMDS
	$(TARGET_CC) $(TARGET_CFLAGS) -std=c99 -pedantic -Wall -Wextra -Wconversion -fPIC -c -o $(@D)/schrift.o $(@D)/schrift.c
	$(TARGET_CC) $(TARGET_LDFLAGS) -shared -o $(@D)/libschrift.so $(@D)/schrift.o
endef

define LIBSCHRIFT_INSTALL_TARGET_CMDS
	$(INSTALL) -D -m 0755 $(@D)/libschrift.so \
		$(TARGET_DIR)/usr/lib/libschrift.so
endef

define LIBSCHRIFT_INSTALL_STAGING_CMDS
	$(INSTALL) -D -m 0755 $(@D)/libschrift.so \
		$(STAGING_DIR)/usr/lib/libschrift.so

	$(INSTALL) -D -m 0644 $(@D)/schrift.h \
		$(STAGING_DIR)/usr/include/schrift.h
endef

$(eval $(generic-package))
