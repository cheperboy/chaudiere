#!/bin/sh
# This script lauch chromium broser un kiosk mode

export DISPLAY=:0

#chromium-browser --kiosk --app=http://chaudiere.local:5007/charts/
chromium-browser --app=http://localhost:5007/charts/

# to kill this process
# killall -9 chromium-browse
