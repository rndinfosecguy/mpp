#!/bin/bash
# Name: stop dns tcpdump
# Description: stops tcpdump to capture dns records on the pine ap interface
# Author: Hy3n4
# Version: 1.0
# Category: interception

# Look for the process ID of a running tcpdump process
tcpdump_pid=$(pgrep -f tcpdump)

# If the process is found, kill it
if [ -n "$tcpdump_pid" ]; then
  LOG "Killing tcpdump process with PID $tcpdump_pid"
  kill $tcpdump_pid
fi