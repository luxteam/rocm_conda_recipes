#!/bin/bash

mkdir -p build

hipcc -D__HIP_PLATFORM_HCC__ -lrocrand -L$TEST_PREFIX/lib src/test_rocrand.cpp -o build/test_rocrand

ROCBLAS_LAYER=0xf TENSILE_DB=0xffff ./build/test_rocrand


