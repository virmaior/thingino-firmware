WIFI_B43_VERSION = $(LINUX_VERSION_PROBED)
WIFI_B43_SITE_METHOD = local
WIFI_B43_VERSION=1.0
WIFI_B43_SITE = $(LINUX_DIR)/drivers/net/wireless/b43

define WIFI_B43_LINUX_CONFIG_FIXUPS
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
	$(call KCONFIG_ENABLE_OPT,CONFIG_SSB_SDIOHOST_POSSIBLE)
	$(call KCONFIG_ENABLE_OPT,CONFIG_SSB_SDIOHOST)
	$(call KCONFIG_SET_OPT,CONFIG_B43=m)
	$(call KCONFIG_ENABLE_OPT,CONFIG_B43_SSB)
	$(call KCONFIG_SET_OPT,CONFIG_B43_SDIO,y)
	$(call KCONFIG_ENABLE_OPT,CONFIG_B43_PIO)
	$(call KCONFIG_ENABLE_OPT,CONFIG_SSB)
	$(call KCONFIG_ENABLE_OPT,CONFIG_SSB_BLOCKIO)
endef

define WIFI_B43_INSTALL_TARGET_CMDS
	$(INSTALL) -D -m 0644 $(WIFI_B43_PKGDIR)/files/fw_bcm43436b0.bin \
		$(TARGET_DIR)/usr/lib/firmware/fw_bcm43436b0.bin

	$(INSTALL) -D -m 0644 $(WIFI_B43_PKGDIR)/files/fw_bcm43438a1.bin \
		$(TARGET_DIR)/usr/lib/firmware/fw_bcm43438a1.bin

	$(INSTALL) -D -m 0644 $(WIFI_B43_PKGDIR)/files/nv_bcm43436b0.txt \
		$(TARGET_DIR)/usr/lib/firmware/nv_bcm43436b0.txt

	$(INSTALL) -D -m 0644 $(WIFI_B43_PKGDIR)/files/nv_bcm43438a1.txt \
		$(TARGET_DIR)/usr/lib/firmware/nv_bcm43438a1.txt
endef

$(eval $(kernel-module))
$(eval $(generic-package))
