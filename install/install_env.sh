#!/bin/bash

########## HOWTO RUN THE SCRIPT ##########
# This will output in terminal and in a log file
#. install_env.sh |& tee install_env.sh.log


############################################ 
# Prerequis
# Install supervisor and nginx
# Clone the repo in /home/pi/Dev/chaudiere 
# and execute the script from here
############################################

DIR_DEV=/home/pi/Dev
DIR_PROD=/home/pi/Prod
DIR_DEV_CHAUDIERE=$DIR_DEV/chaudiere
DIR_PROD_CHAUDIERE=$DIR_PROD/chaudiere
GIT_REPO="https://github.com/cheperboy/chaudiere.git"
OPTION_INSTALL_DEV=false
OPTION_INSTALL_ENV=false

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

# Le scipt doit être exécuté dans un dossier particulier. Veérifier qu'on se trouve dans le bon dossier
if [ $DIR_DEV_CHAUDIERE/install != `pwd` ]
then
	echo "Ce script doit être exécuté dans $DIR_DEV_CHAUDIERE/install"
	return
fi

###############################################
# Create virtualenv and install requirements  #
###############################################
run "deactivate" # deactivate any virtualenv to run next command with system python
say "Create virtualenv prod"
run "rmvirtualenv prod"
run "mkvirtualenv -p python3 prod"
run "/home/pi/Envs/prod/bin/pip3 install -r $DIR_PROD_CHAUDIERE/requirements.txt"

