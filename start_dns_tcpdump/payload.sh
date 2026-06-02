#!/bin/bash
# Name: start dns tcpdump
# Description: starts tcpdump to capture dns records on the pine ap interface
# Author: Hy3n4
# Version: 1.0
# Category: interception

# check if loot directory exists
if [ ! -d "/root/loot/mpp" ]; then
  mkdir -p /root/loot/mpp
fi

# generate unique pcap filename
CAPTURE_FILE="/root/loot/mpp/"
CURRENT_TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
CAPTURE_FILE_CONTENT="${CAPTURE_FILE}${CURRENT_TIMESTAMP}.pcap"
echo "${CAPTURE_FILE_CONTENT}"

# starting tcpdump
LOG "Starting tcpdump for port 53 on wlan0open"
LOG "After stopping tcpdump the result is stored under ${CAPTURE_FILE_CONTENT}"
tcpdump -i wlan0open port 53 -w "${CAPTURE_FILE_CONTENT}" &
