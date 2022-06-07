import os
from argparse import ArgumentParser
from subprocess import check_output
from distutils.dir_util import copy_tree


def copy(args):
    copy_tree(f'/opt/rocm-{args.rocmrelease}/', os.environ['PREFIX'], preserve_symlinks=1)

def install_rocm(args):
    cmd = [
            "sudo",
            "amdgpu-install",
            "-y",
            "--usecase=opencl",
            "--no-dkms",
            "--rocmrelease={}".format(args.rocmrelease),
        ]
    output = check_output(cmd)
    with open('rocm_install.log', 'w') as f:
        f.write(output.decode())
        

def uninstall_rocm(args):
    cmd = [
            "sudo",
            "amdgpu-uninstall",
            "-y",
            "--rocmrelease={}".format(args.rocmrelease),
        ]
    output = check_output(cmd)
    with open('rocm_uninstall.log', 'w') as f:
        f.write(output.decode())
        
        
def make_parser():
    p = ArgumentParser("build.py")
    p.add_argument("--rocmrelease", required=True)
    return p


def main():
    print('Running build')
    parser = make_parser()
    args = parser.parse_args()
    install_rocm(args)
    copy(args)
    uninstall_rocm(args)


if __name__ == "__main__":
    main()