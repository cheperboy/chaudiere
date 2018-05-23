#!/bin/sh

# start_usb.sh

# Arg
# 1: Start
# 0: Stop

sudo /home/pi/Dev/chaudiere/script/usb/uhubctl/uhubctl -p 2 -a $1
 
