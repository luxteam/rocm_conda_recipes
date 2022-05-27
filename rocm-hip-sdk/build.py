import os
from pathlib import Path
from argparse import ArgumentParser
from subprocess import check_output, check_call
import shutil

files_to_patch = [
    {
        'file': os.path.join('hipfft', 'lib', 'cmake', 'hipfft', 'hipfft-targets.cmake'),
        'changes': [('/opt/rocm-{version}', '${_IMPORT_PREFIX}')]
    },
]


def patch_files(args):
    for info in files_to_patch:
        p = Path(os.environ['PREFIX'], info['file']).resolve()
        filedata = p.read_text()
        for change in info['changes']:
            filedata = filedata.replace(change[0].format(version=args.rocmrelease), change[1])
        p.write_text(filedata)
        

def copy(args):
    shutil.copytree(f'/opt/rocm-{args.rocmrelease}/', os.environ['PREFIX'], symlinks=True, dirs_exist_ok=True)


def install_rocm(args):
    cmd = [
            "sudo",
            "amdgpu-install",
            "-y",
            "--usecase=hiplibsdk",
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
    patch_files(args)
    uninstall_rocm(args)


if __name__ == "__main__":
    main()