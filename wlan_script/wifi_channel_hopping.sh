#!/bin/bash

echo "Start Wifi Channel Hopping in 5 seconds."
sleep 5
source /home/hispid/WIFI_INTERFACE_NAME

source /usr/local/bin/chanhop.sh -i $WIFI_INTERFACE -b IEEE80211B -d 5
# source /usr/local/bin/chanhop.sh -i $WIFI_INTERFACE -b IEEE80211A -d 5