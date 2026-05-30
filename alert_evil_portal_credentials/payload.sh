#!/bin/bash
# Title: Evil Portal Credentials Submitted
# Description: checks if new credentials were captured by Evil Portal (needs the Evil Portal payload)
# Author: Hy3n4
# Version: 1.0

# Check if .credentials_md5 exists, and create it if not
if [ ! -f /mmc/root/logs/.credentials_md5 ]; then
  echo "Creating .credentials_md5 for the first time..."
  md5sum /mmc/root/logs/credentials.json > /mmc/root/logs/.credentials_md5
else
  # Calculate MD5 hash of credentials.json and compare it to existing .credentials_md5 content
  current_hash=$(md5sum /mmc/root/logs/credentials.json | cut -d' ' -f1)
  stored_hash=$(cat /mmc/root/logs/.credentials_md5)

  if [ "$current_hash" != "$stored_hash" ]; then
    ALERT "New credentials detected!"
    echo "$current_hash" > /mmc/root/logs/.credentials_md5
  fi
fi
