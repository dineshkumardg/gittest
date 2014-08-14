#!/bin/bash
# ./cho_qa_server.sh start|stop|restart|status
export GAIA_VAR_DIR="/GAIA/cho/var"
export GAIA_PROJECT="CHO"
./qa_server.sh $1
