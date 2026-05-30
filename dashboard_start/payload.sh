#!/bin/bash
# Name: dashboard
# Description: refresh data available and starts the dashboard
# Author: Hy3n4
# Version: 1.0
# Category: interception

export PATH="/mmc/usr/bin:${_PAYLOAD_HOME}/bin:$PATH"
export PYTHONPATH="${_PAYLOAD_HOME}/lib:${_PAYLOAD_HOME}:$PYTHONPATH"
export LD_LIBRARY_PATH="/mmc/usr/lib:${_PAYLOAD_HOME}/lib:$LD_LIBRARY_PATH"

LOG "[*] refreshing database..."
LOG "[*] *************************************"
LOG "[*] *** This may take some time"
LOG "[*] *** Depends on number and size"
LOG "[*] *** of (new) pcap files."
LOG "[*] *** pcap files which were already"
LOG "[*] *** processed in the past will"
LOG "[*] *** not be processed again."
LOG "[*] *************************************"
res=$(python3 setup.py)
LOG "$res"

LOG ""
LOG "[*] Setting up web server"
cd server
python3 -m http.server --cgi 8000 --bind 172.16.52.1 &

LOG ""
LOG "[+] Done! Visit http://172.16.52.1:8000/cgi-bin/dashboard"
