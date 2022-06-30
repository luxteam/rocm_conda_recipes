export HIPDIR=$BUILD_PREFIX/hip
export ARCH=ar
cp make.inc-examples/make.inc.hip-gcc-mkl make.inc
echo 'LIBDIR += -L$(MKLROOT)/lib' >> make.inc
echo 'LIB += -Wl,--enable-new-dtags -Wl,--rpath,$BUILD_PREFIX/lib -Wl,--rpath,$(MKLROOT)/lib -Wl,--rpath,$BUILD_PREFIX/magma/lib' >> make.inc
echo 'DEVCCFLAGS += --gpu-max-threads-per-block=256' >> make.inc
if [[ -n "$PYTORCH_ROCM_ARCH" ]]; then
    amdgpu_targets=`echo $PYTORCH_ROCM_ARCH | sed 's/;/ /g'`
else
    amdgpu_targets=`rocm_agent_enumerator | grep -v gfx000 | sort -u | xargs`
fi
for arch in $amdgpu_targets; do
    echo "DEVCCFLAGS += --amdgpu-target=$arch" >> make.inc
done
# hipcc with openmp flag may cause isnan() on __device__ not to be found; depending on context, compiler may attempt to match with host definition
sed -i 's/^FOPENMP/#FOPENMP/g' make.inc
make -f make.gen.hipMAGMA -j $(nproc)
LANG=C.UTF-8 make lib/libmagma.so -j $(nproc) MKLROOT=$PREFIX
make testing/testing_dgemm -j $(nproc) MKLROOT=$PREFIX