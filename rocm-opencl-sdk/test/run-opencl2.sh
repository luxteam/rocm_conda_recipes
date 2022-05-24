
mkdir -p build

g++ -std=c++17 -o build/test_opencl2 src/test_opencl2.cpp -g -lOpenCL -L$CONDA_PREFIX/lib -I$CONDA_PREFIX/opencl/include -O3

./build/test_opencl2

