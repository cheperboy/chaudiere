#!/bin/bash
export DISPLAY=:0

# get local ip
local_ip_raw=`hostname -I`

#Remove leading whithespace
local_ip="$(echo -e "${local_ip_raw}" | tr -d '[:space:]')"

echo chromium-browser --kiosk --app=http://$local_ip:5007/charts/

# to kill this process
# killall -9 chromium-browse
