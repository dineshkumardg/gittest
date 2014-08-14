#!/bin/sh -x
# source this script in bashrc, then run one of these...
# test_item_deploy_one
# test_item_deploy_many
# test_item_deploy_samples

function test_item_set_ftp_dir {
    if [ "$(uname)" != 'Linux' ]; then
        FTP_ROOT="/c/FTP_ROOT"
        FTP_DIR="$FTP_ROOT/tester/cho/items/all/"
    else
        FTP_ROOT="/home"
        FTP_DIR="$FTP_ROOT/htc/cho/items/all/"
    fi
}

function test_item_deploy_one {
    test_item_set_ftp_dir
    echo "--- Creating ONE test items ------------------------------------"
    ITEMS_DIR="/tmp/,test_items"
    rm -rf $ITEMS_DIR
    scripts_dir="$HOME/GIT_REPOS/gaia/src/scripts/dev" 
    #python $scripts_dir/create_test_items.py --item_type="iaxx" --num_items=1 --num_pages=1 --items_dir $ITEMS_DIR
    python $scripts_dir/create_test_items.py --item_type="meet" --num_items=1 --num_pages=1 --items_dir $ITEMS_DIR

    echo "--- Copying test items to ftp folder -----------------------"
    echo "--- FTP_DIR=$FTP_DIR"
    cp -r $ITEMS_DIR/* $FTP_DIR

    for item_dir in `ls -d  -- $FTP_DIR*/`;   # Note: FTP_DIR MUST have the trailing slash
    do
        echo "--- preparing: item_dir:  '$item_dir' ------------------------------"
        cd $item_dir
        rm -f _status*.txt
        rm -f manifest.md5
        md5sum * > manifest.md5
        touch _status_READY.txt
    done
}

function test_item_deploy_many {
    test_item_set_ftp_dir
    ITEMS_DIR="/tmp/,test_items"
    rm -rf $ITEMS_DIR
    echo "--- Creating test items ------------------------------------"
    #python create_test_items.py --item_type="iaxx" --num_items=1000
    python create_test_items.py --item_type="iaxx" --num_items=7 --num_pages=-1 --items_dir $ITEMS_DIR # inceasing pages
    python create_test_items.py --item_type="meet" --num_items=3 --num_pages=0 --items_dir $ITEMS_DIR # random pages
    # Note: only creates mp3 files for MEET type!...
    python create_test_items.py --item_type="meet" --num_items=2 --num_pages=0  --data_type=Audio --item_start=88 --items_dir $ITEMS_DIR # random pages with mp3 links

    echo "--- Copying test items to ftp folder -----------------------"
    echo "--- FTP_DIR=$FTP_DIR"
    cp -r $ITEMS_DIR/* $FTP_DIR

    for item_dir in `ls -d  -- $FTP_DIR*/`;   # Note: FTP_DIR MUST have the trailing slash
    do
        echo "--- preparing: item_dir:  '$item_dir' ------------------------------"
        cd $item_dir
        rm -f _status*.txt
        rm -f manifest.md5
        md5sum * > manifest.md5
        touch _status_READY.txt
    done
}

function test_item_deploy_samples {
    set_ftp_dir
    # TODO: generalise..for linux..~/GIT_REPOS/data_services...? TODO
    #SAMPLES_DIR="/c/GIT_REPOS/data_services/chatham_house/schema_with_samples"  # change this to suit
    #SAMPLES_DIR="/e/CHO/v1_samples_diax_BUG"  # change this to suit
    SAMPLES_DIR="/e/CHO/v1_samples"  # change this to suit

    echo "--- Copying samples to ftp folder -----------------------"
    echo "--- FTP_DIR=$FTP_DIR"
    cp -r $SAMPLES_DIR/* $FTP_DIR 

    for item_dir in `ls -d  -- $FTP_DIR*/`;   # Note: FTP_DIR MUST have the trailing slash
    do
        echo "--- preparing: item_dir:  '$item_dir' ------------------------------"
        cd $item_dir
        # clean up unwanted files from samples folder
        rm -f _status*.txt
        rm -rf Thumbs.db
        rm -f *.xsd
        rm -f manifest.md5
        rm -rf old\ schemas

        md5sum * > manifest.md5
        touch _status_READY.txt
    done
}

function test_item_deploy_related {
    test_item_set_ftp_dir
    echo "--- Creating 3 RELATED test items ------------------------------------"
    ITEMS_DIR="/tmp/,test_items"
    rm -rf $ITEMS_DIR
    scripts_dir="$HOME/GIT_REPOS/gaia/src/scripts/dev" 
    #python $scripts_dir/create_test_items.py --item_type="iaxx" --num_items=1 --num_pages=1 --items_dir $ITEMS_DIR
    python $scripts_dir/create_test_items.py --create_related=True --items_dir $ITEMS_DIR

    echo "--- Copying test items to ftp folder -----------------------"
    echo "--- FTP_DIR=$FTP_DIR"
    cp -r $ITEMS_DIR/* $FTP_DIR

    for item_dir in `ls -d  -- $FTP_DIR*/`;   # Note: FTP_DIR MUST have the trailing slash
    do
        echo "--- preparing: item_dir:  '$item_dir' ------------------------------"
        cd $item_dir
        rm -f _status*.txt
        rm -f manifest.md5
        md5sum * > manifest.md5
        touch _status_READY.txt
    done
}

