# Install with scripts
1. Install raspbian
2. configure wifi (edit  `/etc/wpa_supplicant/wpa_supplicant.conf`)
3. set hostname to chaudiere (edit  `/etc/hostname`. raspberry will be accessible via *chaudiere.local*)
4. `mkdir /home/pi/Dev && cd /home/pi/Dev` 
5. `git clone https://github.com/cheperboy/chaudiere.git`
6. Secret config 
	- `mkdir /home/pi/CONFIG_CHAUDIERE && touch /home/pi/CONFIG_CHAUDIERE/chaudiere_secret_config.py`
	- or copy template config from repo, edit, and rename (delete 'template')
8. `cd /home/pi/Dev/chaudiere/install` 
9. `. install_system.sh |& tee install_system.sh.log`
10. Add the folowing to ~/.bashrc (virtualenvwrapper config)
	```
	export WORKON_HOME=~/Envs
	export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
	source /home/pi/.local/bin/virtualenvwrapper.sh
	```
	
	`source ~/.bashrc`
11. `sudo /bin/bash hardware.sh |& tee hardware.sh.log`
12. `. install_chaudiere.sh -e |& tee install_chaudiere.sh.log`
13. Create an admin user
	`workon prod && python3 ~/Prod/chaudiere/flask_app/manager.py users create`

## Links
about python3 and virtualenvwrapper see https://medium.com/@gitudaniel/installing-virtualenvwrapper-for-python3-ad3dfea7c717

# Edit config variable

| File | Content | Value |
| ---- | ----- |------|
| `chaudiere_secret_config.py` | `"URL" : "http://xxx.hd.free.fr:",`| Public IP of the network| 
| `flask_app/app/constantes.py` |`InputDb = {TEMP_CHAUDIERE : 'temp0', ...}` | Edit to map Physical inputs to database fields 


# Scripts
 |  | `system.sh` | `hardware.sh` | `install.sh` | `deploy.sh` | 
 | ---- | :-----: | :-----: | :-----: | :-----: | 
 | apt-get update | x |  |  |  | 
 | apt-get dist-upgrade | x |  |  |  | 
 | apt-get upgrade | x |  |  |  | 
 | install supervisor git python-pip nginx | x |  |  |  | 
 | NEXMO install build-essential libssl-dev libffi-dev python-dev | x |  |  |  | 
 | pip install virtualenv virtualenvwrapper | x |  |  |  | 
 | install curl | x |  |  |  | 
 | edit /etc/modules |  | x |  |  | 
 | edit /boot.config.txt |  | x |  |  | 
 | **erase** /home/pi/Prod/chaudiere if exists |  |  | x | x | 
 | create /home/pi/Prod |  |  | x |  | 
 | create /home/pi/Prod/chaudiere |  |  | x |  | 
 | create /home/pi/Prod/db |  |  | x |  | 
 | create /home/pi/Prod/log |  |  | x |  | 
 | create /home/pi/Dev/db |  |  | -d |  | 
 | create /home/pi/Dev/log |  |  | -d |  | 
 | clone repo in Prod/chaudiere |  |  | x | x | 
 | **mkvirtualenv** dev (overwrite) |  |  | -de |  | 
 | install requirements.txt in dev env |  |  | -de |  | 
 | **mkvirtualenv** prod (overwrite) |  |  | -e |  | 
 | install requirements.txt in prod env |  |  | -e |  | 
 | flask_app/manage.py **create_db in prod env** |  |  | x |  | 
 | flask_app/manage.py **create_db in dev env** |  |  | -d |  | 
 | configure nginx |  |  | x |  | 
 | configure supervisor |  |  | x |  | 
 | configure cron (in /etc/cron.d) |  |  | x |  | 
 | supervisorctl start sensor gunicorn |  |  | x | x | 
 | sudo service nginx start |  |  | x | x | 
 


# Directories
``` bash
mkdir ~/Dev
mkdir ~/Dev/log
mkdir ~/Dev/db
mkdir ~/Prod
mkdir ~/Prod/log
mkdir ~/Prod/db
mkdir ~/CONFIG_CHAUDIERE
```

## nginx
Create a chaudiere conf file and sym link

``` bash
sudo cp ~/Prod/chaudiere/config/prod/nginx_chaudiere_conf /etc/nginx/sites-available/

sudo ln -s /etc/nginx/sites-available/nginx_chaudiere_conf /etc/nginx/sites-enabled
```

Remove the sym link to default conf file (otherwise it causes errors)
`sudo rm /etc/nginx/sites-enabled/default`

To test configuration `sudo nginx -t`

To Restart nginx `sudo service nginx restart`

## Supervisor
``` bash
sudo supervisorctl stop all
sudo cp ~/Prod/chaudiere/config/prod/supervisor_chaudiere.conf /etc/supervisor/conf.d/
sudo supervisorctl reread
sudo supervisorctl reload
sudo supervisorctl start sensor gunicorn
```
