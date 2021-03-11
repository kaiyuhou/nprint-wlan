# MAC OS
## Capture WLAN on MAC OS

MAC OS doesn't provide `iw` or `iwconfig` command as Linux. The easiest way to capture wlan packet on mac is using `Wireshark` GUI.

Steps:

- Install & Open `wireshark`:  https://www.wireshark.org/#download
- Click `Capture` -> `Opetions`:
    - The WLAN interface could be `en0` or `en1`
    - Select the `monitor` option at the right most column (only the WLAN interface has this option)
- Start capturing: 
    - the packets should incloud both `Radiotap` header and `802.11` header


Alternative way by command lines

- `tcpdump -Ini en0 -w test.pcap ` or `tshark ...`

## Channel Hopping

- Mannualy Channel Switch
```bash
# Apple undocumented AirPort comment: only for the fisrt time
sudo ln -s /System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport /usr/local/bin/airport 
# turn off wifi connection
sudo airport -z
# switch channel to 161
sudo airport -c161
```

- Auto Channel Hopping
```bash
# auto script
sudo bash mac_wifi_channel_hopping.sh
#
# or call the script directly
# 2.4GHZ, 5 seconds duration 
sudo mac_chanhop.sh -b IEEE80211B -d 5 
# 5GHZ and 2.4GHZ
sudo mac_chanhop.sh -b IEEE80211A -b IEEE80211B -d 5
```