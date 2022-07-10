#!/usr/bin/env bash
set -ex

# remove pyproject.toml
rm $SRC_DIR/pyproject.toml

echo WHICH HIPCC: `which hipcc`
export ROCM_HOME=$PREFIX
export CMAKE_PREFIX_PATH=$PREFIX
export TORCHVISION_INCLUDE="${PREFIX}/include/"
export USE_NINJA=0
export FORCE_CUDA=1
$PYTHON setup.py install