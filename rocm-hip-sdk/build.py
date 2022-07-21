import os
from pathlib import Path
from argparse import ArgumentParser
from subprocess import check_output
from distutils.dir_util import copy_tree
from packaging import version
import glob

config = {
    '>=5.2': {
        'files_to_patch': [
            {
                'file': os.path.join('hipfft', 'lib', 'cmake', 'hipfft-targets.cmake'),
                'changes': [('/opt/rocm-{version}', '${_IMPORT_PREFIX}')]
            }
        ],
        'extra_files': [
            'llvm',
            'share/doc/rocm-llvm',
            'share/doc/rocblas',
            'bin/amdclang*',
            'bin/amdflang',
            'bin/amdlld',
            'lib/librocblas.so.0*',
            'lib/rocblas/library',
        ]
    },
    'default': {
        'files_to_patch': [
            {
                'file': os.path.join('hipfft', 'lib', 'cmake', 'hipfft', 'hipfft-targets.cmake'),
                'changes': [('/opt/rocm-{version}', '${_IMPORT_PREFIX}')]
            }
        ],
        'extra_files': [
            'llvm',
            'rocblas/lib/library',
            'rocblas/lib/librocblas.so.0*',
            'share/doc/rocm-llvm',
            'share/doc/rocblas',
            'bin/amdclang*',
            'bin/amdflang',
            'bin/amdlld',
            'lib/librocblas.so.0*',
            'lib/library/Kernels.so*',
            'lib/library/Tensile*'
        ]
    }
}


def delete_file(path):
    cmd = [
            "sudo",
            "rm",
            "-rf",
            "{}".format(path)
        ]
    print(check_output(cmd))
    

def patch_files(args, cfg):
    if cfg.get('files_to_patch'):
        for info in cfg['files_to_patch']:
            p = Path(os.environ['PREFIX'], info['file']).resolve()
            filedata = p.read_text()
            for change in info['changes']:
                filedata = filedata.replace(change[0].format(version=args.rocmrelease), change[1])
            p.write_text(filedata)
        

def copy(args, cfg):
    rocm_path = f'/opt/rocm-{args.rocmrelease}'
    if cfg.get('extra_files'):
        for ef in cfg['extra_files']:
            for path in glob.glob(os.path.join(rocm_path, ef)):
                delete_file(path)
    copy_tree(rocm_path, os.environ['PREFIX'], preserve_symlinks=1)


def install_rocm(args, cfg):
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
        

def uninstall_rocm(args, cfg):
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
    if version.parse(args.rocmrelease) >= version.parse("5.2"):
        cfg = config['>=5.2']
    else:
        cfg = config['default']
    install_rocm(args, cfg)
    copy(args, cfg)
    patch_files(args, cfg)
    uninstall_rocm(args, cfg)


if __name__ == "__main__":
    main()