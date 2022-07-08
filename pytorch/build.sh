#!/usr/bin/env bash
set -ex

export CMAKE_PREFIX_PATH=$CONDA_PREFIX
export HIP_PATH=$CONDA_PREFIX/hip
export ROCM_PATH=$CONDA_PREFIX
export ROCM_SOURCE_DIR=$CONDA_PREFIX
export USE_NINJA=0
export USE_ROCM=1
export USE_MAGMA=1

which rocminfo
rocminfo
which gcc
gcc --version

rm -rf build
python3 tools/amd_build/build_amd.py
python3 setup.py install