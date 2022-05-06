#!/usr/bin/env bash
set -ex

export CMAKE_PREFIX_PATH=$BUILD_PREFIX
export HIP_PATH=$BUILD_PREFIX/hip
export ROCM_PATH=$BUILD_PREFIX
export ROCM_SOURCE_DIR=$BUILD_PREFIX
export USE_NINJA=0

rm -rf build
python3 tools/amd_build/build_amd.py
python3 setup.py install