import os
from pathlib import Path
from argparse import ArgumentParser
from subprocess import check_output
from distutils.dir_util import copy_tree
from packaging import version
import glob


files_to_patch = {
    '>=5.2': {
        'file': os.path.join('hipfft', 'lib', 'cmake', 'hipfft-targets.cmake'),
        'changes': [('/opt/rocm-{version}', '${_IMPORT_PREFIX}')]
    },
    'default': {
        'file': os.path.join('hipfft', 'lib', 'cmake', 'hipfft', 'hipfft-targets.cmake'),
        'changes': [('/opt/rocm-{version}', '${_IMPORT_PREFIX}')]
    }
}

extra_files = [
    'llvm',
    'rocblas/lib/library',
    'rocblas/lib/librocblas.so.0*',
    'share/doc/rocm-llvm',
    'share/doc/rocblas'
    'bin/amdclang*',
    'bin/amdflang',
    'bin/amdlld',
    'lib/librocblas.so.0*',
    'lib/library/Kernels.so*',
    'lib/library/Tensile*'
]


def delete_file(path):
    cmd = [
            "sudo",
            "rm",
            "-rf",
            "{}".format(path)
        ]
    print(check_output(cmd))
    

def patch_files(args):
    if version.parse(args.rocmrelease) >= version.parse("5.2"):
        ftp = files_to_patch['>=5.2']
    else:
        ftp = files_to_patch['default']
        
    for info in ftp:
        p = Path(os.environ['PREFIX'], info['file']).resolve()
        filedata = p.read_text()
        for change in info['changes']:
            filedata = filedata.replace(change[0].format(version=args.rocmrelease), change[1])
        p.write_text(filedata)
        

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
            "--usecase=hiplibsdk",
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
    patch_files(args)
    uninstall_rocm(args)


if __name__ == "__main__":
    main()