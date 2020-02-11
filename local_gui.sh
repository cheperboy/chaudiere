#!/bin/bash

# Get LAN IP (eg 192.168.0.70)
# Open Chrome browser 

export DISPLAY=:0

# get local ip
local_ip_raw=`hostname -I`
# echo 'local_ip_raw ' -$local_ip_raw-

# Remove IPV6
local_ip="$(echo -e "${local_ip_raw}" | cut -d ' ' -f1)"
# echo 'local_ip ' -$local_ip-

#echo chromium-browser --kiosk --app=http://$local_ip:5007/charts/
chromium-browser --kiosk --app=http://$local_ip:5007/charts/

# to kill this process
# killall -9 chromium-browse
