if [ "$(printf '%s\n' "5.2" "$PKG_VERSION" | sort -V | head -n1)" = "5.2" ]; then 
    unzip $PREFIX/lib/rocblas/library/library.zip -d $PREFIX/lib/rocblas/library
    rm $PREFIX/lib/rocblas/library/library.zip
else
    unzip $PREFIX/rocblas/lib/library/library.zip -d $PREFIX/rocblas/lib/library
    rm $PREFIX/rocblas/lib/library/library.zip
fi