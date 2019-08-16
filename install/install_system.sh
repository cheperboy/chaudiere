#!/bin/bash

########################################################################################
# This script install the required packages with apt-get 
# inspired by this tuto for installation of python3 and virtualenvwrapper 
# https://medium.com/@gitudaniel/installing-virtualenvwrapper-for-python3-ad3dfea7c717
########################################################################################

########## HOWTO RUN THE SCRIPT ##########
# This will output in terminal and in a log file
#. install_system.sh |& tee install_system.sh.log

# This function prints a command and run it
run () {
	echo $1 # print command
	$1 # run command
}

# determine the lenght of the parameter and print it this way
#########
# parameter #
#########
say () {
	length=$(printf "%s" "$1" | wc -c)
	echo
	for i in $( seq 0 $length ); do echo -n =; done; echo;
	echo $1
	for i in $( seq 0 $length ); do echo -n =; done; echo;
}

run "sudo apt-get update"
run "sudo apt-get dist-upgrade -y"
run "sudo apt-get upgrade -y"
run "sudo apt-get -y install supervisor git python3-pip nginx"
# installing virtualenv with sudo apt-get makes it working ok for python2 and python3
run "sudo apt-get -y install virtualenv"
run "pip3 install virtualenvwrapper"

# Specific packages for chaudiere app
run "sudo apt-get install curl"

# Specific packages for i2c
run "sudo apt-get install python-smbus python3-smbus python-dev python3-dev"

# NEXMO need cryptographie and cffi
run "sudo apt-get install build-essential libssl-dev libffi-dev python-dev"

# clean downloaded packages
run "sudo apt-get clean"
