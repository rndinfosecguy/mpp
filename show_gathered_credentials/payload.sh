#!/bin/bash
# Name: Show Gathered Credentials
# Description: Shows credentials which were collected via the evil portal payload
# Author: Hy3n4
# Version: 1.0
# Category: wireless

target_folder="/root/portals/"

# locations where several portals which are compatible with Evil Portal are storing credentials
for item in $(ls -1 $target_folder); do
  if [ -d "$target_folder$item" ]; then
    if [ -f "$target_folder$item/.logs" ]; then
      LOG "Found credential file in $item"
      LOG "------------------------------"
      creds=$(cat "$target_folder$item/.logs")
      LOG "$creds"
      LOG "------------------------------"
      LOG ""
    fi
  fi
done

# location where Evil Portal is storing credentials as said in the documentation (https://github.com/hak5/wifipineapplepager-payloads/tree/master/library/user/evil_portal)
credential_file="/root/logs/credentials.json"
if [ -s "$credential_file" ]; then # Check if the file is not empty
  LOG "Found credentials $credential_file"
  LOG "------------------------------"
  creds=$(cat "$credential_file")
  LOG "$creds"
  LOG "------------------------------"
fi
