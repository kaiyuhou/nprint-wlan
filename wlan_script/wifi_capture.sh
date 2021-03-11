#!/bin/bash

echo "setting up wifi capture"
sleep 5
echo "observing interface " + $WIFI_INTERFACE

while true
do
   echo echo $(date) + " starting wifi capture"
   /usr/sbin/tcpdump -i $WIFI_INTERFACE -z gzip -G 3600 -c 10000000 -w 'trace_%Y%m%d-%H%M%S.pcap' &>> wifi-capture.log
   echo echo $(date) + " END of wifi capture"
done