WIFI_TXW901U_SITE_METHOD = git
WIFI_TXW901U_SITE = https://github.com/gtxaspec/txw901
WIFI_TXW901U_SITE_BRANCH = master
WIFI_TXW901U_VERSION = 136c88fb7ad4cafec43c89b67f8a3653c01c865a
# $(shell git ls-remote $(WIFI_TXW901U_SITE) $(WIFI_TXW901U_SITE_BRANCH) | head -1 | cut -f1)

WIFI_TXW901U_LICENSE = GPL-2.0
WIFI_TXW901U_LICENSE_FILES = COPYING

WIFI_TXW901U_MODULE_MAKE_OPTS = \
	COMPILER=$(TARGET_CROSS) \
	LINUX_KERNEL_PATH=$(LINUX_DIR) \
	ARCH=$(KERNEL_ARCH) \
	CROSS_COMPILE=$(TARGET_CROSS)

define WIFI_TXW901U_LINUX_CONFIG_FIXUPS
	$(call KCONFIG_ENABLE_OPT,CONFIG_WLAN)
	$(call KCONFIG_ENABLE_OPT,CONFIG_WIRELESS)
	$(call KCONFIG_ENABLE_OPT,CONFIG_WIRELESS_EXT)
	$(call KCONFIG_ENABLE_OPT,CONFIG_WEXT_CORE)
	$(call KCONFIG_ENABLE_OPT,CONFIG_WEXT_PROC)
	$(call KCONFIG_ENABLE_OPT,CONFIG_WEXT_PRIV)
	$(call KCONFIG_SET_OPT,CONFIG_CFG80211,y)
	$(call KCONFIG_SET_OPT,CONFIG_MAC80211,y)
	$(call KCONFIG_ENABLE_OPT,CONFIG_MAC80211_RC_MINSTREL)
	$(call KCONFIG_ENABLE_OPT,CONFIG_MAC80211_RC_MINSTREL_HT)
	$(call KCONFIG_ENABLE_OPT,CONFIG_MAC80211_RC_DEFAULT_MINSTREL)
	$(call KCONFIG_SET_OPT,CONFIG_MAC80211_RC_DEFAULT,"minstrel_ht")
endef

define WIFI_TXW901U_BUILD_CMDS
	$(MAKE) -C $(@D) $(WIFI_TXW901U_MODULE_MAKE_OPTS) smac_usb
endef

define WIFI_TXW901U_INSTALL_TARGET_CMDS
	$(INSTALL) -D -m 0644 $(@D)/ko/txw901u.ko \
			$(TARGET_DIR)/lib/modules/$(LINUX_VERSION_PROBED)/extra/txw901u.ko
endef

$(eval $(kernel-module))
$(eval $(generic-package))
