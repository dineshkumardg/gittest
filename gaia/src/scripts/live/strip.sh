#!/bin/bash

# strip.sh > ,strip.log
# save hard disk memory and browser ram; loading of pages likely to be similar; strip can use 2.5gb ram on prod + 50% of a single core
#
# before:
# [jsears@ukandgaia07 ~]$ df /dev/sda1
# Filesystem           1K-blocks      Used Available Use% Mounted on
# /dev/sda1            6338997304 2250836956 3766157816  38% /GAIA
#
# after:
# [gaia@ukandgaia07 cho]$ df /dev/sda1
# Filesystem           1K-blocks      Used Available Use% Mounted on
# /dev/sda1            6338997304 1918535684 4098459088  32% /GAIA
#
#
# head / tail of ,strip.log:
# 2013-09-19 14:52:29 STARTED
# 2013-09-19 14:54:50 /GAIA/cho/web_root/cho_bcrc_1933_0001_000_0000/10126/cho_bcrc_1933_0001_000_0006_thumbnail.jpg
# 2013-09-19 14:54:50 /GAIA/cho/web_root/cho_bcrc_1933_0001_000_0000/10126/cho_bcrc_1933_0001_000_0376_thumbnail.jpg
# ...
# 2013-09-19 23:58:08 /GAIA/cho/web_root/cho_wtxx_1979_0035_000_0000/10346/cho_wtxx_1979_0035_000_0285_thumbnail.jpg
# 2013-09-19 23:58:09 /GAIA/cho/web_root/cho_wtxx_1979_0035_000_0000/10346/cho_wtxx_1979_0035_000_0184_thumbnail.jpg
# 2013-09-19 23:58:09 FINISHED
#
#

tstamp=`date "+%Y-%m-%d %H:%M:%S"`
echo $tstamp STARTED

files=$(find /GAIA/cho/web_root/* -type f -size +10k -name *_thumbnail.jpg)

for file in $files
do
    tstamp=`date "+%Y-%m-%d %H:%M:%S"`
    echo $tstamp $file
    /usr/bin/convert $file -resize 128x128 -strip $file
done

tstamp=`date "+%Y-%m-%d %H:%M:%S"`
echo $tstamp FINISHED