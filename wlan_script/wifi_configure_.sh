#!/bin/bash

WIFI_INTERFACE=wlx74da38f2d22e

echo "sleep 5 seconds"
sleep 20

echo $(date) + " - configuring wifi interface $WIFI_INTERFACE to monitormode"
/sbin/ifconfig $WIFI_INTERFACE down
/sbin/iwconfig $WIFI_INTERFACE mode monitor
/sbin/ifconfig $WIFI_INTERFACE up
