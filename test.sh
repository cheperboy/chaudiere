#!/bin/bash

run () {
	echo $1 # print command
	$1 # run command
}

# Create sym link
# run "sudo chown"
# run "sudo ln -s /home/pi/Dev/chaudiere/config/prod/chaudiere_cron.txt /etc/cron.d"
run "sudo cp /home/pi/Dev/chaudiere/config/prod/test_cron_conf /etc/cron.d"
run "sudo chown root /etc/cron.d/test_cron_conf"
