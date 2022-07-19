import os
from argparse import ArgumentParser
from subprocess import check_output, check_call
from distutils.dir_util import copy_tree
from packaging import version
import glob

files_to_delete = [
    'Kernels.so-000-gfx1010.hsaco',
    'Kernels.so-000-gfx1011.hsaco',
    'Kernels.so-000-gfx1012.hsaco',
    'Kernels.so-000-gfx1030.hsaco',
    'Kernels.so-000-gfx803.hsaco',
    'Kernels.so-000-gfx900.hsaco',
    'Kernels.so-000-gfx906-xnack-.hsaco',
    'Kernels.so-000-gfx908-xnack-.hsaco',
    'Kernels.so-000-gfx90a-xnack+.hsaco',
    'Kernels.so-000-gfx90a-xnack-.hsaco',
    'TensileLibrary.dat',
    'TensileLibrary_gfx1030.co',
    'TensileLibrary_gfx1030.dat',
    'TensileLibrary_gfx803.co',
    'TensileLibrary_gfx803.dat',
    'TensileLibrary_gfx900.co',
    'TensileLibrary_gfx900.dat',
    'TensileLibrary_gfx906.co',
    'TensileLibrary_gfx906.dat',
    'TensileLibrary_gfx908.co',
    'TensileLibrary_gfx908.dat',
    'TensileLibrary_gfx90a.co',
    'TensileLibrary_gfx90a.dat',
]

def copy(args):
    if version.parse(args.rocmrelease) >= version.parse("5.2"):
        rocblas_library_path = "lib/rocblas/library"
    else:
        rocblas_library_path = "rocblas/lib/library"
    cmd = [
            "sudo",
            "zip",
            "-rj",
            "/opt/rocm-{}/{}/library.zip".format(args.rocmrelease, rocblas_library_path),
            "/opt/rocm-{}/{}".format(args.rocmrelease, rocblas_library_path),
        ]
    check_call(cmd)
    for ftd in files_to_delete:
        cmd = [
            "sudo",
            "rm",
            "-f",
            "/opt/rocm-{}/{}/{}".format(args.rocmrelease, rocblas_library_path, ftd),
        ]
        check_call(cmd)
    copy_tree(f'/opt/rocm-{args.rocmrelease}/', os.environ['PREFIX'], preserve_symlinks=1)
    cmd = [
            "sudo",
            "rm",
            "/opt/rocm-{}/{}/library.zip".format(args.rocmrelease, rocblas_library_path)
        ]
    check_call(cmd)

def install_rocblas(args):
    cmd = [
            "apt",
            "download",
            "rocblas{}".format(args.rocmrelease),
        ]
    check_call(cmd)
    deb_pkg_name = glob.glob("rocblas{}*.deb".format(args.rocmrelease))[0]
    cmd = [
            "sudo",
            "dpkg",
            "-i",
            "--force-depends",
            deb_pkg_name
        ]
    output = check_output(cmd)
    with open('rocblas_install.log', 'w') as f:
        f.write(output.decode())
        

def uninstall_rocblas(args):
    cmd = [
            "sudo",
            "apt",
            "remove",
            "-y",
            "rocblas{}".format(args.rocmrelease),
        ]
    output = check_output(cmd)
    with open('rocblas_uninstall.log', 'w') as f:
        f.write(output.decode())
        
        
def make_parser():
    p = ArgumentParser("build.py")
    p.add_argument("--rocmrelease", required=True)
    return p


def main():
    print('Running build')
    parser = make_parser()
    args = parser.parse_args()
    install_rocblas(args)
    copy(args)
    uninstall_rocblas(args)


if __name__ == "__main__":
    main()