#!/bin/bash

########## HOWTO RUN THE SCRIPT ##########
# This will output in terminal and in a log file
#. install_chaudiere.sh |& tee install_chaudiere.sh.log
# option -d : Also install /Dev environnement
# option -e : Also install virtual environnement for both Dev and Prod (mkvirtualenv, pip install -r requirements.txt)

##################################
# Get options -d -e with getopts #
##################################
DEV=false
envi=false

OPTIND=1 # Reset getopts (in case the script was called previously)
while getopts :de opt; do
    case $opt in 
        d) DEV=true;;
        e) envi=true;;
        :) echo "Missing argument for option -$OPTARG"; return;;
       \?) echo "Unknown option -$OPTARG"; return;;
    esac
done

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

if [ "$DEV" = true ] ; then
    echo 'dev is true'
fi
if [ "$DEV" = true ] && [ "$envi" = true ] ; then
    echo 'DEV & ENV is true'
fi

