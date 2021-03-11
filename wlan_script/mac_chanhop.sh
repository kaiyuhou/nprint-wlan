#!/bin/bash
#
# New Version: Support Mac OS
# Author: Kaiyu
# Update: 2021-03-11
#
# Orignal Version: Support Linux
# https://gist.github.com/hnw/6fbd3ac3bb59d0c93fc0bd2a823cf5cb
# Channel hopping shell script
# GPLv2
# Portions of code graciously taken from Bill Stearns defragfile
# http://www.stearns.org/defragfile/
# jwright@hasborg.com

# For the first time use
# sudo ln -s /System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport /usr/local/bin/airport 

# Defaults
BANDS="IEEE80211B"
DWELLTIME=".25"

CHANB="1 6 11 2 7 3 8 4 9 5 10"
CHANBJP="1 13 6 11 2 12 7 3 8 14 4 9 5 10"
CHANBINTL="1 13 6 11 2 12 7 3 8 4 9 5 10"
# CHANA="36 40 44 48 52 56 60 149 153 157 161"
CHANA="36 40 44 48 52 56 60 64 100 104 108 112 116 120 124 128 132 136 140 144 149 153 157 161 165"

fail () {
	while [ -n "$1" ]; do
		echo "$1" >&2
		shift
	done
	echo "Exiting." >&2
	echo
	exit 1
} #End of fail

usage () {
	fail 'chanhop.sh: Usage:' \
	 "$0 [-i|--interface] [-b|--band] [-d|--dwelltime]" \
	 '-i or --interface specifies the interface name to hop on [optional for Mac OS]' \
	 '-b or --band specifies the bands to use for channel hopping, one of' \
	 '	IEEE80211B 	Channels 1-11 [default]' \
	 '	IEEE80211BINTL	Channels 1-13' \
	 '	IEEE80211BJP	Channels 1-14' \
	 '	IEEE80211A	Channels 36-161' \
	 '    Use multiple -b arguments for multiple channels' \
	 "-d or --dwelltime amount of time to spend on each channel [default $DWELLTIME seconds]" \
	 ' ' \
	 "e.x. $0 -i ath0 -b IEEE80211BINTL -b IEEE80211A -d .10"
 } #End of usage

if [ `whoami` != root ]; then
	echo "You must run this script as root, or under \"sudo\"."
	usage
	fail
fi


while [ -n "$1" ]; do
	case "$1" in
	-i|--interface)
		INTERFACE="$2"
		shift
		;;
	-b|--band)
		ARG_BANDS="$2 $ARG_BANDS"
		shift
		;;
	-d|--dwelltime)
		ARG_DWELLTIME="$2"
		shift
		;;
	*)
		echo "Unsupported argument \"$1\"."
		usage
		fail
		;;
	esac
	shift
done

# Test the sleep duration value
if [ ! -z "$ARG_DWELLTIME" ] ; then
	sleep $ARG_DWELLTIME 2>/dev/null
	if [ $? -ne 0 ] ; then
		fail "Invalid dwell time specified: \"$ARG_DWELLTIME\"."
	fi
	DWELLTIME=$ARG_DWELLTIME
fi

# If the user specified the -b argument, we use that instead of default
if [ ! -z "$ARG_BANDS" ] ; then
	BANDS=$ARG_BANDS
fi

# Expand specified bands into a list of channels
for BAND in $BANDS ; do
	case "$BAND" in
	IEEE80211B|IEEE80211b|ieee80211b)
		CHANNELS="$CHANNELS $CHANB"
		;;
	IEEE80211BJP|IEEE80211bjp|ieee80211bjp)
		CHANNELS="$CHANNELS $CHANBJP"
		;;
	IEEE80211BINTL|IEEE80211bintl|ieee80211bintl)
		CHANNELS="$CHANNELS $CHANBINTL"
		;;
	IEEE80211A|IEEE80211a|ieee80211a)
		CHANNELS="$CHANNELS $CHANA"
		;;
	*)
		fail "Unsupported band specified \"$BAND\"."
		;;
	esac
done

echo "Stop wifi connection"
airport -z

echo "Starting channel hopping, press CTRL/C to exit."
while true; do
	for CHANNEL in $CHANNELS ; do
		airport -c$CHANNEL
		if [ $? -ne 0 ] ; then
			fail "error when setting channel $CHANNEL"
		fi
		sleep $DWELLTIME
	done
done