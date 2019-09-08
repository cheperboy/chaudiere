# -*- coding: utf-8 -*-
import subprocess
import re
from flask import current_app as app
from app import db

########
# Nexmo
########

import nexmo

def nexmo_balance():
    nexmo_client = nexmo.Client(key=app.config['NEXMO_API_KEY'], secret=app.config['NEXMO_API_SECRET'])
    result = nexmo_client.get_balance()    
    balance = "{:.2f}".format(result['value'])
    balance = str(balance) + " €"
    return (balance)

########
# Network
########
def hostname():
    cmd = """cat /etc/hostname"""
    stdout = subprocess.check_output(cmd, shell=True)
    stdout = stdout.decode('utf-8')
    return (stdout)

def ip_lan_eth():
    cmd = """ifconfig eth0 | grep 'inet ' | awk '{print $2}' """
    stdout = subprocess.check_output(cmd, shell=True)
    stdout = stdout.decode('utf-8')
    return (stdout)

def ip_lan_wifi():
    cmd = """ifconfig wlan0 | grep 'inet ' | awk '{print $2}' """
    stdout = subprocess.check_output(cmd, shell=True)
    stdout = stdout.decode('utf-8')
    return (stdout)

########
# Supervisor
########
def supervisor_status():
    """
    """
    cmd = '''sudo supervisorctl status'''
    stdout = subprocess.check_output(cmd, shell=True)
    stdout = stdout.decode('utf-8')
    procs = stdout.splitlines() # each line is a process
    result = {}
    for proc in procs:
        proc = re.sub('\s+', ' ', proc).strip() #replace multiple spaces by one space
        splitted_proc = proc.split(' ')
        name = splitted_proc.pop(0)
        status = splitted_proc.pop(0)
        uptime = ' '.join(splitted_proc)
        result[name] = status + '  ' + uptime
    return (result)

########
# System
########
def system_uptime():
    """
    """
    cmd = '''uptime -p'''
    stdout = subprocess.check_output(cmd, shell=True)
    stdout = stdout.decode('utf-8')
    return (stdout)

def system_date():
    """
    """
    cmd = '''date'''
    stdout = subprocess.check_output(cmd, shell=True)
    stdout = stdout.decode('utf-8')
    return (stdout)

def cpu_temp():
    """
    The shell command (vcgencmd measure_temp) returns
    temp=64.5'C
    This function returns
    64.5'C
    """
    cmd = '''vcgencmd measure_temp'''
    stdout = subprocess.check_output(cmd, shell=True)
    stdout = stdout.decode('utf-8')
    stdout = stdout.split("=")
    return(stdout[1])

def disk_space():
    """
    The shell command (df with options...) returns
    /dev/root          7,0G    3,5G  52%
    This function returns
    {'cpu_temp': '7,0G', 'used': '3,5G', 'used_percent': '52%'}    
    """
    cmd = '''df -h --output=source,size,used,pcent | grep /dev/root'''
    stdout = subprocess.check_output(cmd, shell=True)
    stdout = stdout.decode('utf-8')
    stdout = stdout.split( )
    ret = {"size" : stdout[1], "used": stdout[2], "used_percent": stdout[3]}
    return (ret)
    
########
# Database
########
def db_size():
    """
    The command returns:
        EMPTY LINE
        app.db 0
        chaudiere.db 536576
        chaudiere_hour.db 8192
        chaudiere_minute.db 241664        
    This function returns:
        {'app.db': '0 Mo', 'chaudiere.db': '537 Mo', 'chaudiere_hour.db': '8 Mo', 'chaudiere_minute.db': '242 Mo'}
    """
    cmd = """ls -l /home/pi/"""+app.config['ENVNAME']+"""/db | awk '{ print $9 " " $5 }' """
    stdout = subprocess.check_output(cmd, shell=True)
    stdout = stdout.decode('utf-8')
    ret = {}
    for line in stdout.splitlines():
        line = line.split( )
        if len(line) > 0:
            size = "{:.0f}".format(int(line[1])/(1000*1000))
            size = str(size) + " Mo"
            ret[line[0]] = size
    return (ret)

    