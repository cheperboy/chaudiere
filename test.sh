#!/bin/bash

run () {
	echo $1 # print command
	$1 # run command
}

# Copy template conf file in /etc/cron.d
run "sudo cp /home/pi/Dev/chaudiere/config/prod/chaudiere_cron.txt /etc/cron.d"
# file in /etc/cron.d must be owned by root
run "sudo chown root /etc/cron.d/chaudiere_cron.txt"
