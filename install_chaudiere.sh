#!/bin/bash

########## HOWTO RUN THE SCRIPT ##########
# This will output in terminal and in a log file
#. install_chaudiere.sh |& tee install_chaudiere.sh.log

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
if [ $DIR_DEV_CHAUDIERE != `pwd` ]
then
	echo "Ce script doit être exécuté dans $DIR_DEV_CHAUDIERE"
	return
fi

# Vérifie que nginx est installé
if ! [ -f /usr/sbin/nginx ] ; then 
	echo "nginx not installed"
	return
fi
# Vérifie que supervisor est installé
if ! [ -f /usr/bin/supervisorctl ] ; then 
	echo "supervisor not installed"
	return
fi

# Vérifie que chaudiere_secret_config.py existe
if ! [ -f ~/CONFIG_CHAUDIERE/chaudiere_secret_config.py ] ; then 
	echo "~/CONFIG_CHAUDIERE/chaudiere_secret_config.py not found"
	return
fi

# Alerte avant d'exécuter l'installation
echo "/!\ NGINX AND SUPERVISOR CONF WILL BE OVERWRITTEN !"
echo "ctrl C to exit now!"
sleep 4

###################
# Stop nginx and supervisor #
###################
say "Stop nginx and supervisor"
run "sudo supervisorctl stop gunicorn sensor"
run "sudo service nginx stop"

##############
# Create Directories #
##############
say "Create Directories"
run "rm -rf  $DIR_PROD_CHAUDIERE"
run "mkdir $DIR_PROD"
run "mkdir $DIR_PROD/log"
run "mkdir $DIR_PROD/db"
run "mkdir $DIR_PROD_CHAUDIERE"

run "mkdir $DIR_DEV/log"
run "mkdir $DIR_PROD/db"

##############
# Clone repo in Prod #
##############
say "Clone repo in Prod"
run "git clone $GIT_REPO $DIR_PROD_CHAUDIERE"

############################
# Create virtualenv and install requirements  #
############################
say "Create virtualenv dev"

run "deactivate" # deactivate any virtualenv to run next command with system python
run "mkvirtualenv dev"
run "/home/pi/Envs/dev/bin/pip install -r $DIR_DEV_CHAUDIERE/requirements.txt"

say "Create virtualenv prod"
run "mkvirtualenv prod"
run "/home/pi/Envs/prod/bin/pip install -r $DIR_PROD_CHAUDIERE/requirements.txt"

####################
# Create chaudiere databases  #
####################
say "Create chaudiere databases" 
run "/home/pi/Envs/dev/bin/python $DIR_DEV_CHAUDIERE/flask_app/manage.py create_db"
run "/home/pi/Envs/prod/bin/python $DIR_PROD_CHAUDIERE/flask_app/manage.py create_db"

#############
# Configure nginx #
#############
say "Configure nginx"
# Copy template conf file
run "sudo cp $DIR_PROD_CHAUDIERE/config/prod/nginx_chaudiere_conf /etc/nginx/sites-available/"

# Create sym link
run "sudo ln -s /etc/nginx/sites-available/nginx_chaudiere_conf /etc/nginx/sites-enabled"

# Remove the sym link to default conf file
run "sudo rm /etc/nginx/sites-enabled/default"

# Test nginx conf
run "sudo nginx -t"

################
# Configure supervisor #
################
say "Configure supervisor"
run "sudo supervisorctl stop all"
run "sudo cp $DIR_PROD_CHAUDIERE/config/prod/supervisor_chaudiere.conf /etc/supervisor/conf.d/"


##############
# Configure Crontab #
##############
say "Configure Crontab"
# Copy template conf file in /etc/cron.d
run "sudo cp $DIR_PROD_CHAUDIERE/config/prod/chaudiere_cron.txt /etc/cron.d"
# file in /etc/cron.d must be owned by root
run "sudo chown root /etc/cron.d/chaudiere_cron.txt"

###################
# Start nginx and supervisor #
###################
say "Start nginx and supervisor"
run "sudo supervisorctl reread"
run "sudo supervisorctl reload"
run "sudo supervisorctl start sensor gunicorn"

run "sudo supervisorctl status"
run "sudo service nginx start"
sleep 2
run "sudo service nginx status"

