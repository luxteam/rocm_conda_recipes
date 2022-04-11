import os
from argparse import ArgumentParser
from subprocess import check_output
import shutil


def copy(args):
    shutil.copytree(f'/opt/rocm-{args.rocmrelease}/', os.environ['PREFIX'], symlinks=True, dirs_exist_ok=True)

def install_rocm(args):
    cmd = [
            "sudo",
            "apt",
            "install",
            "-y",
            "rocrand{}".format(args.rocmrelease),
        ]
    output = check_output(cmd)
    with open('rocrand_install.log', 'w') as f:
        f.write(output.decode())
        

def uninstall_rocm(args):
    cmd = [
            "sudo",
            "apt",
            "remove",
            "-y",
            "rocrand{}".format(args.rocmrelease),
        ]
    output = check_output(cmd)
    with open('rocrand_uninstall.log', 'w') as f:
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