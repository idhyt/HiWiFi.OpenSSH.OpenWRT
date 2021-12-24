# hiwifi.openssh

Script to open HiWiFi ssh

when I ssh to my HiWiFi, get a refused:
```
ssh: connect to host 192.168.41.1 port 22: Connection refused
```
I write this script to open ssh for lazy man like me...

very very thanks http://www.hiwifi.wtf/

Note I only testing it in my HiWiFi, the system version is **HC5661A - 1.4.10.20837s**

```
pip install requests
python hiwifi.ssh.py -H {host_ip}
```

open ssh success like this:

```
╰─ python hiwifi.ssh.py -H 192.168.41.1
[+] uuid: 12345678-1234-5678-1234-123456789012
[+] local token: RDRFRTA3NEE123456789NzaCwxNTY0MjE3MT123456789/i2a1hZBWqmA123456789
[+] cloud token: yaELY8i123456789n9QXOtYw=
[+] Success: ssh port is 22
```

# flash openwrt (HC5661A)

upload [uboot](./openwrt/breed-mt7628-hiwifi-hc5661a.bin) and flash

```
mtd write -r breed-mt7628-hiwifi-hc5661a.bin u-boot
```

rebooting...hold reset 3s...

breed Web: 192.168.1.1

firmware update -> firmware -> [openwrt-sysupgrade](./openwrt/openwrt-ramips-mt76x8-hiwifi_hc5661a-squashfs-sysupgrade.bin) -> enjoy!

