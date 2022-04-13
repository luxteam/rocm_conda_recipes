import os
from argparse import ArgumentParser
from subprocess import check_output, check_call
import shutil


def copy(args):
    shutil.copytree(f'/opt/rocm-{args.rocmrelease}/', os.environ['PREFIX'], symlinks=True, dirs_exist_ok=True)

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
    # copy(args)
    uninstall_rocblas(args)


if __name__ == "__main__":
    main()