import os
from argparse import ArgumentParser
from subprocess import check_output, check_call
from distutils.dir_util import copy_tree
import glob

def copy(args):
    copy_tree(f'/opt/rocm-{args.rocmrelease}/', os.environ['PREFIX'], preserve_symlinks=1)
    

def install_rocmllvm(args):
    cmd = [
            "apt",
            "download",
            "rocm-llvm{}".format(args.rocmrelease),
        ]
    check_call(cmd)
    deb_pkg_name = glob.glob("rocm-llvm{}*.deb".format(args.rocmrelease))[0]
    cmd = [
            "sudo",
            "dpkg",
            "-i",
            "--force-depends",
            deb_pkg_name
        ]
    output = check_output(cmd)
    with open('rocmllvm_install.log', 'w') as f:
        f.write(output.decode())
        

def uninstall_rocmllvm(args):
    cmd = [
            "sudo",
            "apt",
            "remove",
            "-y",
            "rocm-llvm{}".format(args.rocmrelease),
        ]
    output = check_output(cmd)
    with open('rocmllvm_uninstall.log', 'w') as f:
        f.write(output.decode())
        
        
def make_parser():
    p = ArgumentParser("build.py")
    p.add_argument("--rocmrelease", required=True)
    return p


def main():
    print('Running build')
    parser = make_parser()
    args = parser.parse_args()
    install_rocmllvm(args)
    copy(args)
    uninstall_rocmllvm(args)


if __name__ == "__main__":
    main()