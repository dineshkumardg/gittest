#!/bin/sh
source_root="`pwd`";
out_dir="`pwd`/../mp3_items_PREPARED";

# does not work with brackets or whitespace in the filename

echo "please make sure you use the same content provider as the other half of the incomplete item"

for fpath in `find . -name "*.mp3" -print`;
do
    mp3_fname="`basename "$fpath"`";
    mp3_name="${mp3_fname%\.*}"; # file name without ext
    item_name="${mp3_name}";
    item_dir="${out_dir}/${mp3_name}";
    echo "--- ----------------------------------------";
    echo "--- fpath='$fpath'";
    echo "--- mp3_fname='$mp3_fname'";
    echo "--- mp3_name ='$mp3_name'";
    echo "--- item_name='$item_name'";
    echo "--- item_dir='$item_dir'";

    mkdir $item_dir;
    cp $fpath $item_dir;
    cd $item_dir;
    md5sum * > manifest.md5;
    touch _status_READY.txt;
    cd $source_root;
done

#rm -f _status*.txt
#rm -f manifest.md5

