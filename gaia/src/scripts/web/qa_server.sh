#!/bin/bash

function setup {
    if [[ -n "${1}" ]]  # if arg1 "is not null"
    then
        COMMAND="${1}";
    fi

    # arg2 should be used to set GAIA_PROJECT in a live environment,
    # in dev-environments, we will pre-set GAIA_PROJECT to make our lives easier.
    if [[ -n "${2}" ]]  # if arg2 "is not null"
    then
        GAIA_PROJECT="${2}";
    elif [[ -z "${GAIA_PROJECT}" ]] # elif GAIA_PROJECT "is zero-length" (is null)
    then    
        echo "Please provide a config name in the argument" #no args, no env. var. for gaia_proj (exit)
        exit 1
    fi

    #GAIA_VAR_DIR="./var"   # set this in dev envs
    if [[ -z "${GAIA_VAR_DIR}" ]] # if GAIA_VAR_DIR "is zero-length" (is null)
    then
        GAIA_VAR_DIR="/var";
    fi

    PID_FILE="$GAIA_VAR_DIR/run/gaia/qa_app_server_${GAIA_PROJECT}.pid"
}

function print_setup {
    echo "Settings"
    echo "--------"
    echo "  COMMAND=$COMMAND"
    echo "  GAIA_PROJECT=$GAIA_PROJECT"
    echo "  GAIA_VAR_DIR=$GAIA_VAR_DIR"
    echo "  PID_FILE=$PID_FILE"
    echo ""
}

setup $*

case "$COMMAND" in
start)
    if [ -e "$PID_FILE" ] # if pid file exists...
    then
        PID="`cat $PID_FILE`"
        
        # if process with pid exists... (kill -0 is special: tests if signal can be sent; ie if process exists, and can send signal)
        #if kill -0 $PID > /dev/null 2>&1
        if kill -0 $PID >& /dev/null
        then
            echo "NOT STARTING: OLD SERVER is UP (PID: $PID): please use restart intsead."
            exit 1
        fi
    fi

    NOW="`date +%Y_%m_%d_%H_%M_%N`"
    python ./server/run_server.py ${GAIA_PROJECT} >& $GAIA_VAR_DIR/log/gaia/qa_server_${GAIA_PROJECT}_${NOW}.log &
    if [ $? -eq 0 ]
    then
        PID=$!
        echo $PID > $PID_FILE
        echo "Started new QA App Server for project ${GAIA_PROJECT}, pid=${PID}"
    else
        print_setup
        echo "FAILED to start QA App Server for project ${GAIA_PROJECT}"
        echo "failed command:"
        echo " python ./server/run_server.py ${GAIA_PROJECT} >& $GAIA_VAR_DIR/log/gaia/qa_server_${GAIA_PROJECT}_${NOW}.log &"
        exit 2
    fi
;;

stop)
    if [ -e "$PID_FILE" ] # if pid file exists...
    then
        PID="`cat $PID_FILE`"

        # if process with pid exists... (kill -0 is special: tests if signal can be sent; ie if process exists, and can send signal)
        if kill -0 $PID > /dev/null 2>&1
        then
            echo "killing old QA App server for project ${GAIA_PROJECT}, pid=${PID}"
            kill $PID
            rm $PID_FILE
        fi
    fi
;;

restart)
    $0 stop  $GAIA_PROJECT
    $0 start $GAIA_PROJECT
;;

status)
    if [ -e "$PID_FILE" ] # if pid file exists...
    then
        PID="`cat $PID_FILE`"

        # if process with pid exists... (kill -0 is special: tests if signal can be sent; ie if process exists, and can send signal)
        #if kill -0 $PID > /dev/null 2>&1
        if kill -0 $PID >& /dev/null
        then
            echo "UP: QA App server for project ${GAIA_PROJECT} is RUNNING with pid=${PID}";
            exit 0
        else
            echo "DOWN: QA App server for project ${GAIA_PROJECT} is NOT running with pid=${PID}";
            exit 9
        fi
    else
        echo "DOWN: QA App server for project ${GAIA_PROJECT} is NOT running (no pid file in GAIA_VAR_DIR=$GAIA_VAR_DIR)";
    fi
;;

make_dev_dirs)
    mkdir -pv $GAIA_VAR_DIR/log/gaia
    mkdir -pv $GAIA_VAR_DIR/run/gaia
;;

*)
    print_setup
    echo "Developer Usage"
    echo "---------------"
    echo "in a DEV environment, set these in your ~/.bashrc:"
    echo "  export GAIA_VAR_DIR=\"$HOME/GAIA_WORKING_DIR/var\""
    echo "  export GAIA_PROJECT=\"TUSH_LINUX\""
    echo "then run this:"
    echo "  $0 make_dev_dirs"
    echo ""
    echo "Normal Usage"
    echo "------------"
    echo "  $0 [start|stop|restart|status] GAIA_PROJECT"
    echo ""
    echo "eg"
    echo "  $0 restart TUSH_LINUX"
    echo ""
    exit 1
esac

