#!/bin/bash
# Name: show dns traffic
# Description: shows the traffic captured in a previous dns capture.
# Author: Hy3n4
# Version: 1.0
# Category: interception

export PATH="/mmc/usr/bin:${_PAYLOAD_HOME}/bin:$PATH"
export PYTHONPATH="${_PAYLOAD_HOME}/lib:${_PAYLOAD_HOME}:$PYTHONPATH"
export LD_LIBRARY_PATH="/mmc/usr/lib:${_PAYLOAD_HOME}/lib:$LD_LIBRARY_PATH"

if [ ! -d "/mmc/root/loot/mpp/" ]; then
  ERROR_DIALOG "Error: /mmc/root/loot/mpp/ does not exist."
  exit 0
fi

pcap_files=($(find /mmc/root/loot/mpp/ -type f -name "*.pcap" -print))

if [ ${#pcap_files[@]} -eq 0 ]; then
  ERROR_DIALOG "No pcap files found in /mmc/root/loot/mpp/."
  exit 0
fi

options=()

for file in "${pcap_files[@]}"; do
    if [[ "$file" =~ \.pcap$ ]]; then
    options+=("$(basename "$file")")
    fi
done

# Pick first file as default
default="${options[0]}"

selection=$(LIST_PICKER "Choose Payload" "${options[@]}" "$default") || exit 0
LOG "Selected: $selection"
LOG "It may take some time depending on the file size."
LOG "-------------------------------------------------"

res=$(python3 analyze.py /mmc/root/loot/mpp/"$selection")
LOG "$res"
