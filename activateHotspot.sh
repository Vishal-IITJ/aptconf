#!/bin/bash

check_hotspot_exists() {
    nmcli connection show | grep -q 'RASPI'
}

create_hotspot() {
    sudo nmcli connection add type wifi ifname wlan0 con-name RASPI autoconnect yes ssid RASPI
    sudo nmcli connection modify RASPI 802-11-wireless.mode ap 802-11-wireless.band bg ipv4.method shared
    sudo nmcli connection modify RASPI 802-11-wireless-security.key-mgmt wpa-psk
    sudo nmcli connection modify RASPI 802-11-wireless-security.psk "00000000"
}

activate_hotspot() {
    sudo nmcli device wifi rescan
    sudo nmcli connection up RASPI
}

if ! check_hotspot_exists; then
    create_hotspot
fi

activate_hotspot
