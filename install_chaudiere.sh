#!/bin/sh

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

# Le scipt doit être exécuté dans un dossier particulier. Veérifier qu'on se trouve dans le bon dossier
if [ $DIR_DEV_CHAUDIERE != `pwd` ]
then
	echo "Ce script doit être exécuté dans $DIR_DEV_CHAUDIERE"
	return
fi

echo "/!\ NGINX AND SUPERVISOR CONF WILL BE ERASED !"
echo "ctrl C to exit now!"
sleep 4

#############################
# Stop nginx and supervisor #
#############################
echo "stop nging and supervisor"
sudo supervisorctl stop gunicorn sensor
sudo service nginx stop

######################
# Create Directories #
######################
mkdir $DIR_PROD
mkdir $DIR_PROD/log
mkdir $DIR_PROD/db
mkdir $DIR_PROD_CHAUDIERE

mkdir $DIR_DEV/log
mkdir $DIR_PROD/db

######################
# Clone repo in Prod #
######################
echo "clone $GIT_REPO $PROD_DIR"
git clone $GIT_REPO $DIR_PROD_CHAUDIERE
echo ""

######################
# Install virtualenv #
######################
workon prod
pip install -r $DIR_PROD_CHAUDIERE/requirements.txt


###################
# Create database #
###################
python flask_app/manage.py create_db

###################
# Configure nginx #
###################
# Copy template conf file
sudo cp $DIR_PROD_CHAUDIERE/config/prod/nginx_chaudiere_conf /etc/nginx/sites-available/

# Create sym link
sudo ln -s /etc/nginx/sites-available/nginx_chaudiere_conf /etc/nginx/sites-enabled

# Remove the sym link to default conf file
sudo rm /etc/nginx/sites-enabled/default

# Test nginx conf
sudo nginx -t

########################
# Configure supervisor #
########################
sudo supervisorctl stop all
sudo cp $DIR_PROD_CHAUDIERE/config/prod/supervisor_chaudiere.conf /etc/supervisor/conf.d/


#####################
# Configure Crontab #
#####################
#write out current crontab
crontab -l > tempcron
#echo new cron into cron file
echo $DIR_PROD_CHAUDIERE/config/prod/cron.txt >> tempcron
#install new cron file
crontab tempcron
rm tempcron

echo "\n Check this new crontab"
crontab -l

##############################
# Start nginx and supervisor #
##############################
echo "start nging and supervisor"
sudo supervisorctl reread
sudo supervisorctl reload
sudo supervisorctl start sensor gunicorn

sudo supervisorctl status
sudo service nginx start
sudo service nginx status

