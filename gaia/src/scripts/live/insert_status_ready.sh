#!/bin/bash

#
# Script is meant to be used on ukandgaia07 (or a developer machine)
#
# i.e. 
#   ./insert_status_ready.sh '/home/htc/cho/items/all/cho*'
#  
# Aim of the script is to insert _status_READY.txt into all folders inside $1 ONLY
# as long as the _status_READY.txt is not already present.
#

if [ $# -eq 0 ]
  then
    echo 'No path supplied' 
    exit 1
    fi
if [ -z "$1" ]
  then
    echo 'No path supplied' 
    exit 1
fi

FILE_TO_INSERT='_status_READY.txt'
START=`date --rfc-3339='ns'`
echo "$START START inserting $FILE_TO_INSERT if not already present"

FOLDERS=`find $1 -type d`

for FOLDER in $FOLDERS 
do
    if [ ! -f $FOLDER/$FILE_TO_INSERT ]; then
        echo "putting $FILE_TO_INSERT into $FOLDER"
        touch $FOLDER/$FILE_TO_INSERT
    fi
done

END=`date --rfc-3339='ns'`
echo "$END END"
