#!/bin/bash
# Name: stop dashboard
# Description: stops the dashboard
# Author: Hy3n4
# Version: 1.0

# Look for the process ID of a running tcpdump process
python_pid=$(pgrep -f python)

# If the process is found, kill it
if [ -n "$python_pid" ]; then
  LOG "Killing python web server process with PID $python_pid"
  kill $python_pid
fi
