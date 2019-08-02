#!/bin/sh
DIR_DEV_CHAUDIERE=/home/pi/Dev/chaudiere
DIR_PROD_CHAUDIERE=/home/pi/Prod/chaudiere
GIT_REPO="https://github.com/cheperboy/chaudiere.git"

# Le scipt doit être exécuté dans un dossier particulier. Veérifier qu'on se trouve dans le bon dossier
if [ $DIR_DEV_CHAUDIERE != `pwd` ]
then
	echo "Ce script doit être exécuté dans $DIR_DEV_CHAUDIERE"
	exit 1
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
