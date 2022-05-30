#!/bin/bash

mkdir -p build

hipcc -D__HIP_PLATFORM_HCC__ -lrocblas -L$CONDA_PREFIX/lib src/test_rocblas.cpp -o build/test_rocblas

ROCBLAS_LAYER=0xf TENSILE_DB=0xffff ./build/test_rocblas


