#!/bin/bash 

#
# Script is meant to be used on ukandgaia07 (or a developer machine)
#
# i.e. 
#   ./create_new_manifest.sh '/home/jsears/Desktop/all/*'
#  
# Aim of the script is, in any subfolder of $1, to:
# 1. delete manifest.md5 and _status_READY.txt files
# 2. create a new manifest.md5 and, afterwards, a new _status_READY.txt file
#

START_DIR="$1"

if [ -z $START_DIR ]
  then
    echo 'No path supplied, using current dir' 
    START_DIR="."
fi


MANIFEST_FNAME='manifest.md5'
STATUS_FNAME='_status_READY.txt'
START=`date --rfc-3339='ns'`
echo "$START START"

FOLDERS=`find $START_DIR -type d`
#FOLDERS=`ls`
echo "FOLDERS=$FOLDERS"
echo "STARTING_DIR=$START_DIR"

cd $START_DIR
for FOLDER in $FOLDERS 
do
        echo "rebuild $MANIFEST_FNAME then recreate $STATUS_FNAME in $FOLDER"
        cd $FOLDER
        rm -f $MANIFEST_FNAME
        rm -f $STATUS_FNAME

        md5sum * > $MANIFEST_FNAME
        touch $STATUS_FNAME
        cd ..
done

END=`date --rfc-3339='ns'`
echo "$END END"
