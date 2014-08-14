#!/bin/sh
# a noddy convenience script (for Big Ears).
FTP_ROOT="/c/FTP_ROOT"  # change this to suit
FTP_DIR="$FTP_ROOT/tester/stha/items/all/"
SAMPLES_DIR="/c/TUSH_DATA/STHA/20111116/STHA_20111116_01/STHA/1827/"


echo "--- Copying STHA samples to ftp folder -----------------------"
echo "--- FTP_DIR=$FTP_DIR"
cp -r $SAMPLES_DIR/* $FTP_DIR

for item_dir in `ls -d  -- $FTP_DIR*/`;   # Note: FTP_DIR MUST have the trailing slash
do
    echo "--- preparing: item_dir:  '$item_dir' ------------------------------"
    cd $item_dir
    rm -f manifest.md5
    rm _status*

    md5sum * > manifest.md5
    touch _status_READY.txt
done

