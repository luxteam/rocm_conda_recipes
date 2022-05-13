### Requirements
- Fulfilled requirements for installing ROCm via amdgpu-install (must support ROCm v5.1.0 installation)
- Installed anaconda/miniconda with conda-build package (`conda install conda-build`)

To build a package, execute (this will require root access as we are using amdgpu-install)
```bash
conda build /path/to/recipe/dir
```


After the build is complete
```bash
conda install --use-local <package-name>
```

