#!/bin/bash

##########################
# This script updates the Prod repository #
# Shall be run after install_chaudiere.sh  #
##########################

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


DIR_DEV_CHAUDIERE=/home/pi/Dev/chaudiere
DIR_PROD_CHAUDIERE=/home/pi/Prod/chaudiere
GIT_REPO="https://github.com/cheperboy/chaudiere.git"

# Le scipt doit être exécuté dans un dossier particulier. Veérifier qu'on se trouve dans le bon dossier
if [ $DIR_DEV_CHAUDIERE != `pwd` ]
then
	echo "Ce script doit être exécuté dans $DIR_DEV_CHAUDIERE"
	return
fi

echo "stop nging and supervisor"
sudo supervisorctl stop gunicorn sensor
sudo service nginx stop

echo "clean dir $DIR_PROD_CHAUDIERE"
rm -rf $DIR_PROD_CHAUDIERE
mkdir $DIR_PROD_CHAUDIERE

echo "clone $GIT_REPO $PROD_DIR"
git clone $GIT_REPO $DIR_PROD_CHAUDIERE
echo ""

echo "start nging and supervisor"
sudo supervisorctl start gunicorn sensor
sudo supervisorctl status
sudo service nginx start
sudo service nginx status
