#!/bin/bash

echo "Start Mac OS Wifi Channel Hopping in 5 seconds."
sleep 5

if [ ! -f "/usr/local/bin/airport" ]; then
	echo "AirPort does not exist, ln a new one"
	ln -s /System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport /usr/local/bin/airport
fi

source mac_chanhop.sh -b IEEE80211B -d 5
# source chanhop.sh -b IEEE80211A -d 5