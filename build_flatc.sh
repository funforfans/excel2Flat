#! /bin/bash

MYLODER=$(cd `dirname ${0}`; pwd)
DIST_BIN="${MYLODER}/flatc/"

# install flatbuffer source code
git clone https://github.com/google/flatbuffers.git
cd flatbuffers
cmake -G "Unix Makefiles" -DCMAKE_BUILD_TYPE=Release
make -j2
if [ ! -d ${DIST_BIN} ]; then
    echo ${DIST_BIN}
    mkdir ${DIST_BIN}
fi
cp flatc ${DIST_BIN}
cd ${MYLODER}
echo "build flatbuffer bins done !"