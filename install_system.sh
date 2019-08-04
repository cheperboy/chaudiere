#!/bin/bash

# This function prints a command and run it
run () {
	echo $1 # print command
	$1 # run command
}

run "sudo apt-get update"
run "sudo apt-get dist-upgrade -y"
run "sudo apt-get upgrade -y"
run "sudo apt-get -y install supervisor git python-pip nginx"
run "pip install virtualenv virtualenvwrapper"

# Specific packages for chaudiere app

run "sudo apt-get install curl"

# NEXMO need cryptographie and cffi
run "sudo apt-get install build-essential libssl-dev libffi-dev python-dev"

# clean downloaded packages
run "sudo apt-get clean"


