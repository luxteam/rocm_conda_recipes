#!/bin/bash
PACKAGE_NAME=$1
BUILD_DIR=${2:-../build_logs}

export DEBIAN_FRONTEND=noninteractive

pwd
conda build --debug $PACKAGE_NAME 2>&1 | tee $BUILD_DIR/$PACKAGE_NAME\_$(date +"%I:%M_%d%m%Y").log

