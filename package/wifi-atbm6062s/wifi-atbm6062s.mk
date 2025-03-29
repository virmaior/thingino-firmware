WIFI_ATBM6062S_SITE_METHOD = git
WIFI_ATBM6062S_SITE = https://github.com/gtxaspec/atbm-wifi
WIFI_ATBM6062S_SITE_BRANCH = atbm606x
WIFI_ATBM6062S_VERSION = 09e7f713e8c4c3e74a19568f4aada4398fad9181
# $(shell git ls-remote $(WIFI_ATBM6062S_SITE) $(WIFI_ATBM6062S_SITE_BRANCH) | head -1 | cut -f1)

WIFI_ATBM6062S_LICENSE = GPL-2.0

ATBM6062S_MODULE_NAME = "atbm6062s"

WIFI_ATBM6062S_MODULE_MAKE_OPTS = \
	KDIR=$(LINUX_DIR)

define WIFI_ATBM6062S_LINUX_CONFIG_FIXUPS
	$(call KCONFIG_ENABLE_OPT,CONFIG_WLAN)
	$(call KCONFIG_ENABLE_OPT,CONFIG_WIRELESS)
	$(call KCONFIG_ENABLE_OPT,CONFIG_WIRELESS_EXT)
	$(call KCONFIG_ENABLE_OPT,CONFIG_WEXT_CORE)
	$(call KCONFIG_ENABLE_OPT,CONFIG_WEXT_PROC)
	$(call KCONFIG_ENABLE_OPT,CONFIG_WEXT_PRIV)
	# Must disable kernel's CFG80211, driver provides it's own.
	$(call KCONFIG_DISABLE_OPT,CONFIG_CFG80211)
	$(call KCONFIG_SET_OPT,CONFIG_MAC80211,y)
	$(call KCONFIG_ENABLE_OPT,CONFIG_MAC80211_RC_MINSTREL)
	$(call KCONFIG_ENABLE_OPT,CONFIG_MAC80211_RC_MINSTREL_HT)
	$(call KCONFIG_ENABLE_OPT,CONFIG_MAC80211_RC_DEFAULT_MINSTREL)
	$(call KCONFIG_SET_OPT,CONFIG_MAC80211_RC_DEFAULT,"minstrel_ht")
endef

LINUX_CONFIG_LOCALVERSION = $(shell awk -F "=" '/^CONFIG_LOCALVERSION=/ {print $$2}' $(BR2_LINUX_KERNEL_CUSTOM_CONFIG_FILE))

define WIFI_ATBM6062S_INSTALL_CONFIGS
	$(INSTALL) -m 0755 -d $(TARGET_DIR)/lib/modules/3.10.14$(LINUX_CONFIG_LOCALVERSION)
	touch $(TARGET_DIR)/lib/modules/3.10.14$(LINUX_CONFIG_LOCALVERSION)/modules.builtin.modinfo

	$(INSTALL) -m 0755 -d $(TARGET_DIR)/usr/share/wifi
	$(INSTALL) -m 0644 -t $(TARGET_DIR)/usr/share/wifi \
		$(WIFI_ATBM_WIFI_PKGDIR)/files/*.txt

	$(INSTALL) -D -m 0644 $(@D)/firmware/cronus_SDIO_NoBLE_SDIO_svn19514_24M_wifi6phy_DCDC.bin \
		$(TARGET_DIR)/lib/firmware/$(call qstrip,$(ATBM6062S_MODULE_NAME))_fw.bin
endef

WIFI_ATBM6062S_POST_INSTALL_TARGET_HOOKS += WIFI_ATBM6062S_INSTALL_CONFIGS

define WIFI_ATBM6062S_COPY_CONFIG
	$(INSTALL) -D -m 0644 $(@D)/configs/atbm6062s.config \
		$(@D)/.config
endef

WIFI_ATBM6062S_PRE_CONFIGURE_HOOKS += WIFI_ATBM6062S_COPY_CONFIG

$(eval $(kernel-module))
$(eval $(generic-package))
