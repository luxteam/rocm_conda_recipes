#!/usr/bin/env bash
set -ex

export CMAKE_PREFIX_PATH=$PREFIX
export HIP_PATH=$PREFIX/hip
export ROCM_PATH=$PREFIX
export ROCM_SOURCE_DIR=$PREFIX
export CFLAGS+=-I$PREFIX/roctracer/include
export USE_NINJA=OFF
export USE_ROCM=ON

rm -rf build
python tools/amd_build/build_amd.py
python setup.py install