#!/bin/bash

FILES=*
for f in $FILES
do
    if [[ $f == cho_* ]]
    then
        FILE=$(basename $f .xml)
        mv $f /mnt/UKDEV/pgref/$FILE
    fi
done
