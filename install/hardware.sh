#!/bin/bash

########## HOWTO RUN THE SCRIPT ##########
# sudo /bin/bash hardware.sh

####################################
# This script configure /etc/modules and /boot/config.txt #
####################################

# This function prints a command and run it
run () {
	echo $1 # print command
	$1 # run command
}

say () {
	length=$(printf "%s" "$1" | wc -c)
	echo
	for i in $( seq 0 $length ); do echo -n =; done; echo;
	echo $1
	for i in $( seq 0 $length ); do echo -n =; done; echo;
}

DIR_DEV=/home/pi/Dev
DIR_DEV_CHAUDIERE=$DIR_DEV/chaudiere

##################
# Configure  /etc/modules #
##################
say "This is append to /etc/modules"
cat $DIR_DEV_CHAUDIERE/config/prod/etc_modules
sudo cat $DIR_DEV_CHAUDIERE/config/prod/etc_modules >> /etc/modules

##################
# Configure  /etc/modules #
##################
say "This is append to /boot/config.txt"
cat $DIR_DEV_CHAUDIERE/config/prod/boot_config.txt
sudo cat $DIR_DEV_CHAUDIERE/config/prod/boot_config.txt >> /boot/config.txt

say "REBOOT to apply new configuration"

