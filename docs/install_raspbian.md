# Raspbian Install & Configure

## Flash SD Card
1. Format SD card FAT32
2. Download [Raspbian](https://www.raspberrypi.org/downloads/raspbian/)
3. Flash image with [Etcher](https://www.balena.io/etcher/)
4. Create a file `boot/ssh` before booting raspbian to enable ssh

## Wifi setup before first boot
[help](https://howchoo.com/g/ndy1zte2yjn/how-to-set-up-wifi-on-your-raspberry-pi-without-ethernet)

Create file `boot/wpa_supplicant.conf`. (Raspbian will move it in `/etc/wpa_supplicant/` when the system is booted)

!!! warning
    EOL Conversion shall be **UNIX File Format**.

Add content:
``` bash
country=FR
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={
    ssid="YOUR_NETWORK_NAME"
    psk="YOUR_PASSWORD"
}
```

## Wifi setup after first boot
If conf is done after first boot, edit wpa_supplicant.conf  
`sudo nano /etc/wpa_supplicant/wpa_supplicant.conf`
```shell
network={
    ssid="YOUR_NETWORK_NAME"
    psk="YOUR_PASSWORD"
    key_mgmt=WPA-PSK
}
```

## Configuration
### Hostname and password
1.  Modify hostname, Edit `/etc/hostname`. Set to chaudiere (recognized on network as *chaudiere.local*)
2.  Modify pi password `sudo passwd pi`
 
### Package install
**Update/upgrade system and existing packages**

`sudo apt-get update` met à jour la liste des dépôts

`sudo apt-get dist-upgrade -y` met à jour tous les paquets installés vers les dernières versions en installant de nouveaux paquets si nécessaire

`sudo apt-get upgrade -y` met à jour tous les paquets installés sur le système

**Install packages**

`sudo apt-get -y install supervisor git python-pip nginx`

`pip install virtualenv virtualenvwrapper`

[tuto virtualenv](https://virtualenvwrapper.readthedocs.io/en/latest/install.html)

**specific packages for chaudiere app**

`sudo apt-get install curl`

NEXMO need cryptographie and cffi

`sudo apt-get install build-essential libssl-dev libffi-dev python-dev`

**clean**

`sudo apt-get clean` supprime les paquets téléchargés et stockés sur carte SD


### bashrc
`nano ~/.bashrc`

``` bash
# ls alias
alias ll='ls -l'
alias la='ls -A'
alias lla='ls -la'
alias l='ls -CF'

# supervisor alias
alias restart_all='sudo supervisorctl restart all'
alias status='sudo supervisorctl status'
alias start_script='sudo supervisorctl start script'
alias stop_script='sudo supervisorctl stop script'

# other alias
alias dev='cd /home/pi/Dev/chaudiere/'
alias prod='cd /home/pi/Prod/chaudiere/'

# load virtualenvwrapper for python (after custom PATHs)
export WORKON_HOME=~/Envs
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
source /home/pi/.local/bin/virtualenvwrapper.sh


# workon dev env when the consol is open 
workon dev
```

### Configure firewall
see [tuto](https://www.tecmint.com/setup-ufw-firewall-on-ubuntu-and-debian/)

**Chaudiere config**

allow ssh, samba, 5007tcp

**Usefull commands**

* `sudo apt-get install ufw` - Install
* `sudo ufw status numbered` - List rules 
* `sudo ufw enable` - Enable Firewall (may break ssh connection, allow ssh rule first)
* `sudo ufw disable` - Disable Firewall

**Enable by application name**

* `sudo ufw app list` - List applications
* `sudo ufw allow ssh` - Enable app ssh (on default port 22)

**Enable a specific port**

* `sudo ufw allow 2222/tcp` - Enable tcp ssh port 2222 

