#!/bin/bash

# find . -name '*.xml' -exec  grep seriesNumber {} \;
FILES=$(find . -name '*.xml')
for f in $FILES
do
    # sed '/seriesNumber/d' $f > $f.new
    # diff $f $f.new
    rm -f $f
    mv $f.new $f
done
