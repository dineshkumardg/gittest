#!/bin/bash

# affected types are chrx and rpax
CMYK_FILES=( $(find . -name 'cho_chrx*.jpg' -not -name '*thumbnail.jpg' -and -not -name '*.CMYK.*' -print -exec identify -format '%[colorspace]' {} \; | paste -s -d ".\n" | grep CMYK | sort))
NUMBER_OF_FILES=${#CMYK_FILES[@]}
echo "Found ${NUMBER_OF_FILES} CMYK files"

COUNTER=0
for CMYK_FILE in ${CMYK_FILES[@]}
do
    COUNTER=$((COUNTER+1))

    # remove last 5 characters
    # echo ${CMYK_FILE} | sed 's/.\{5\}$//'
    FNAME=$(sed 's/.\{5\}$//' <<< ${CMYK_FILE} )
    
    NOW=$(date +'%Y%m%d%H%M%S')
    echo "${NOW} ${COUNTER}/${NUMBER_OF_FILES} ${FNAME}"

    # backup original file 
    cp -f ${FNAME} "${FNAME}.CMYK.jpg"

    # replace file with correct colorspace
    convert -colorspace RGB ${FNAME} "${FNAME}.RGB.jpg"
    rm -f ${FNAME}
    mv "${FNAME}.RGB.jpg" ${FNAME}

	# remove the backup
	rm -f "${FNAME}.RGB.jpg"
done
