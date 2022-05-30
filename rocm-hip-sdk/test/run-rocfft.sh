#!/bin/bash

mkdir -p build

hipcc -D__HIP_PLATFORM_HCC__ -lrocfft -lhipfft -L$CONDA_PREFIX/lib src/test_rocfft.cpp -o build/test_rocfft

ROCBLAS_LAYER=0xf TENSILE_DB=0xffff ./build/test_rocfft


