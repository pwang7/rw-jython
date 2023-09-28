#!/usr/bin/env bash

set -o errexit
set -o nounset
set -o xtrace

VERSION="2023.1.3"
RWJAR="./rapidwright-$VERSION-standalone-lin64.jar"

if [ -f $RWJAR ]; then
    echo "$RWJAR exits, no need to download"
else
    # wget https://github.com/Xilinx/RapidWright/releases/download/v2023.1.0-beta/rapidwright-2023.1.0-standalone-lin64.jar
    wget "https://github.com/Xilinx/RapidWright/releases/download/v$VERSION-beta/$RWJAR"
fi
