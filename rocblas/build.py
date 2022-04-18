import os
from argparse import ArgumentParser
from subprocess import check_output, check_call
import shutil

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
    'TensileLibrary_gfx803.co',
    'TensileLibrary_gfx900.co',
    'TensileLibrary_gfx906.co',
    'TensileLibrary_gfx908.co',
    'TensileLibrary_gfx90a.co',
]

def copy(args):
    cmd = [
            "sudo",
            "zip",
            "-rj",
            "/opt/rocm-{}/rocblas/lib/library/library.zip".format(args.rocmrelease),
            "/opt/rocm-{}/rocblas/lib/library".format(args.rocmrelease),
        ]
    check_call(cmd)
    for ftd in files_to_delete:
        cmd = [
            "sudo",
            "rm",
            "/opt/rocm-{}/rocblas/lib/library/{}".format(args.rocmrelease, ftd),
        ]
        check_call(cmd)
    shutil.copytree(f'/opt/rocm-{args.rocmrelease}/', os.environ['PREFIX'], symlinks=True, dirs_exist_ok=True)
    cmd = [
            "sudo",
            "rm",
            "/opt/rocm-{}/rocblas/lib/library/library.zip".format(args.rocmrelease)
        ]
    check_call(cmd)

def install_rocblas(args):
    cmd = [
            "apt",
            "download",
            "rocblas{}".format(args.rocmrelease),
        ]
    check_call(cmd)
    cmd = [
            "sudo",
            "dpkg",
            "-i",
            "--force-depends",
            "rocblas5.1.0_2.43.0.50100-36_amd64.deb"
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