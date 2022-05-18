#!/bin/bash

mkdir -p build

rm build/test_rocblas2

hipcc -D__HIP_PLATFORM_HCC__ -lrocblas -L$CONDA_PREFIX/lib src/test_rocblas2.cpp -o build/test_rocblas2

ROCBLAS_LAYER=0xf TENSILE_DB=0xffff ./build/test_rocblas2


