# script archive_minute.py

## Summary

Python script used to store average values (one per Minute) of Chaudiere Database.
supposed to be run every 1 or 2 minutes by cron

## CLI Usage

### Normal mode

    python archive_minute.py
    
search for last ChaudiereMinute entry.
start from this entry to create a ChaudiereMinute entry per minute, logging average values of Chaudiere

### rework_from_now mode

    python archive_minute.py --rework_from_now --hours N
    
rework N hours from current datetime

### rework_from_date

    python archive_minute.py --rework_from_date  --hours N --date YYYY/MM/DD/HH

### CRON Config

Run every odd minutes

    1-59/2 * * * * /home/pi/Envs/dev/bin/python /home/pi/Dev/chaudiere/chaudiereapp/scripts/archive_minute.py


## ToDo

Rework modes shall delete existing entries before creating new ones


# script process_phase.py

## Summary

python script used to process phase value of ChaudiereMinute entries.
supposed to be run every 1 or 2 minutes by cron

## CLI Usage :

Idem archive_minute.py

## CRON Config :

    1-59/2 * * * * /home/pi/Envs/dev/bin/python /home/pi/Dev/chaudiere/chaudiereapp/scripts/process_phase.py
