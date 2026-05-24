#!/bin/bash

PAYLOAD_DIR="/root/payloads/user/mpp/show_dns_traffic"

export PATH="/mmc/usr/bin:$PAYLOAD_DIR/bin:$PATH"
export PYTHONPATH="$PAYLOAD_DIR/lib:$PAYLOAD_DIR:$PYTHONPATH"
export LD_LIBRARY_PATH="/mmc/usr/lib:$PAYLOAD_DIR/lib:$LD_LIBRARY_PATH"

options=()

for file in /mmc/root/loot/mpp/*; do
    [ -f "$file" ] || continue
    options+=("$(basename "$file")")
done

# Pick first file as default
default="${options[0]}"

selection=$(LIST_PICKER "Choose Payload" "${options[@]}" "$default") || exit 0
LOG "Selected: $selection"
LOG "--------------------"

res=$(python3 analyze.py /mmc/root/loot/mpp/"$selection")
LOG "$res"
