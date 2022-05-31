
mkdir -p build

g++ -std=c++17 -o build/test_opencl src/test_opencl.cpp -g -lOpenCL -L$CONDA_PREFIX/opencl/lib -I$CONDA_PREFIX/opencl/include -O3

./build/test_opencl

