
mkdir -p build

g++ -std=c++17 -o build/test_opencl3 src/test_opencl3.cpp src/Timer.cpp -g -lOpenCL -L$CONDA_PREFIX/opencl/lib -I$CONDA_PREFIX/opencl/include -O3

./build/test_opencl3

