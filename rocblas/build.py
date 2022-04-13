import os
from argparse import ArgumentParser
from subprocess import check_output
import shutil


def copy(args):
    shutil.copytree('/home/georgiy/Desktop/Viacheslav/rocblas/rocBLAS/build/release/rocblas-install', os.environ['PREFIX'], symlinks=True, dirs_exist_ok=True)


def make_parser():
    p = ArgumentParser("build.py")
    p.add_argument("--rocmrelease", required=True)
    return p


def main():
    print('Running build')
    parser = make_parser()
    args = parser.parse_args()
    copy(args)


if __name__ == "__main__":
    main()