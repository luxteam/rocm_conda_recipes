import os
from argparse import ArgumentParser
from subprocess import check_output
from distutils.dir_util import copy_tree
import glob


extra_files = [
    'llvm',
    'share/doc/rocm-llvm',
    'bin/amdclang*',
    'bin/amdflang',
    'bin/amdlld'
]


def delete_file(path):
    cmd = [
            "sudo",
            "rm",
            "-rf",
            "{}".format(path)
        ]
    print(check_output(cmd))
    

def copy(args):
    rocm_path = f'/opt/rocm-{args.rocmrelease}'
    for ef in extra_files:
        for path in glob.glob(os.path.join(rocm_path, ef)):
            delete_file(path)
    copy_tree(rocm_path, os.environ['PREFIX'], preserve_symlinks=1)


def install_rocm(args):
    cmd = [
            "sudo",
            "amdgpu-install",
            "-y",
            "--usecase=openclsdk",
            "--no-dkms",
            "--rocmrelease={}".format(args.rocmrelease),
        ]
    output = check_output(cmd)
    with open('rocm_install.log', 'w') as f:
        f.write(output.decode())
        

def uninstall_rocm(args):
    output = ""
    cmd = [
            "sudo",
            "amdgpu-uninstall",
            "-y",
            "--rocmrelease={}".format(args.rocmrelease),
        ]
    try:
        output = check_output(cmd).decode()
    except:
        print('Error during ROCm uninstallation. Trying one more time')
        output += check_output(cmd).decode()
    with open('rocm_uninstall.log', 'w') as f:
        f.write(output)
        

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