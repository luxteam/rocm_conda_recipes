#!/bin/bash
PACKAGE_NAME=$1
BUILD_DIR=${2:-../build_logs}

export DEBIAN_FRONTEND=noninteractive

mkdir -p $BUILD_DIR
pwd
conda build --debug -c defaults -c conda-forge $PACKAGE_NAME 2>&1 | tee $BUILD_DIR/$PACKAGE_NAME\_$(date +"%m%d%Y_%I:%M").log

