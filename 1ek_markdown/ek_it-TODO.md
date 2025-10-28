# server mac address 
cerberos: BC:A5:11:0D:22:56
athena: 00:1D:09:7B:3C:ED
hera: B0:83:FE:79:08:1E

# add to uci 
uci set luci.sauth.sessiontime='9000'
uci set luci-opkg.sauth.sessiontime='9000'

# delete from uci
uci delete network.lan.ip6assign
uci delete openvpn_recipes.server_tun_ptp
uci delete openvpn_recipes.server_tun
uci delete openvpn_recipes.server_tap_bridge
uci delete dhcp.lan.ra
uci delete dhcp.lan.dhcpv6
uci delete dhcp.lan.dynamicdhcp
uci delete dhcp.lan.ra_slaac
uci delete dhcp.lan.dns_service
uci delete firewall.wg
