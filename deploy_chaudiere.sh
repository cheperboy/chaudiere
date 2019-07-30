#!/bin/sh

# Shall be run inside 
PROD_DIR=/home/pi/Prod
CHAUDIERE_DIR=$PROD_DIR/chaudiere
GIT_REPO="https://github.com/cheperboy/chaudiere.git"
 
echo "stop gunicorn and sensor script"
sudo supervisorctl stop gunicorn script
echo "stop nginx"
sudo service nginx stop

echo "remove dir $CHAUDIERE_DIR"
rm -rf $CHAUDIERE_DIR

echo "clone git repo $GIT_REPO"
git clone $GIT_REPO


echo "start gunicorn and sensor script"
sudo supervisorctl start gunicorn script
echo "start nginx"
sudo service nginx start
sudo supervisorctl status

