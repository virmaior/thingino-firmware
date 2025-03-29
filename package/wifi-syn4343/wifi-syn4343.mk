WIFI_SYN4343_SITE_METHOD = git
WIFI_SYN4343_SITE = https://github.com/acvigue/bcmdhd
WIFI_SYN4343_SITE_BRANCH = main
WIFI_SYN4343_VERSION = a874170026892c58352a5be37c4c0f1f6767f295
# $(shell git ls-remote $(WIFI_SYN4343_SITE) $(WIFI_SYN4343_SITE_BRANCH) | head -1 | cut -f1)

WIFI_SYN4343_MODULE_MAKE_OPTS = \
	KVER=$(LINUX_VERSION_PROBED) \
	KSRC=$(LINUX_DIR) \
	CONFIG_BCMDHD=m \
	CONFIG_BCMDHD_SDIO=y \
	CONFIG_BCMDHD_OOB=y \
	CONFIG_CFG80211=y \
	CONFIG_BCMDHD_AG=y

define WIFI_SYN4343_LINUX_CONFIG_FIXUPS
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

define WIFI_SYN4343_INSTALL_TARGET_CMDS
	$(INSTALL) -D -m 0644 $(WIFI_SYN4343_PKGDIR)/files/fw_bcm43436b0.bin \
		$(TARGET_DIR)/usr/lib/firmware/fw_bcm43436b0.bin

	$(INSTALL) -D -m 0644 $(WIFI_SYN4343_PKGDIR)/files/fw_bcm43438a1.bin \
		$(TARGET_DIR)/usr/lib/firmware/fw_bcm43438a1.bin

	$(INSTALL) -D -m 0644 $(WIFI_SYN4343_PKGDIR)/files/nv_bcm4343.txt \
		$(TARGET_DIR)/usr/lib/firmware/nv_bcm4343.txt
endef

$(eval $(kernel-module))
$(eval $(generic-package))
