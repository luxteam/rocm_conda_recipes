if [ "$(printf '%s\n' "5.2" "$PKG_VERSION" | sort -V | head -n1)" = "5.2" ]; then 
    rm -f $PREFIX/lib/rocblas/library/*
else
    rm -f $PREFIX/rocblas/lib/library/*
fi