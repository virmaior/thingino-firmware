WIFI_SSV6158_SITE_METHOD = git
WIFI_SSV6158_SITE = https://github.com/wltechblog/wifi-ssv6158
WIFI_SSV6158_SITE_BRANCH = main
WIFI_SSV6158_VERSION = 01e200f1bdb9072b12f9b68765d8616adcdb6c84
# $(shell git ls-remote $(WIFI_SSV6158_SITE) $(WIFI_SSV6158_SITE_BRANCH) | head -1 | cut -f1)

WIFI_SSV6158_LICENSE = GPL-2.0
WIFI_SSV6158_LICENSE_FILES = COPYING

WIFI_SSV6158_MODULE_MAKE_OPTS = \
	KSRC=$(LINUX_DIR)

define WIFI_SSV6158_LINUX_CONFIG_FIXUPS
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

define WIFI_SSV6158_COPY_CONFIG
	$(INSTALL) -D -m 0644 $(WIFI_SSV6158_PKGDIR)/files/ssv6x5x-wifi.cfg \
		$(TARGET_DIR)/usr/share/wifi/ssv6x5x-wifi.cfg
endef

WIFI_SSV6158_PRE_CONFIGURE_HOOKS += WIFI_SSV6158_COPY_CONFIG

$(eval $(kernel-module))
$(eval $(generic-package))
