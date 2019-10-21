#! /bin/bash

MYLODER=$(cd `dirname ${0}`; pwd)
DIST_BIN="${MYLODER}/dist/"
RUN_BIN="${DIST_BIN}run"

pyinstaller -F run.py

if [ -d ${DIST_BIN} ];
then
    echo $RUN_BIN
    `cp ${RUN_BIN} ${MYLODER}`
else
    echo "error!"
fi
echo "run bin done !"


