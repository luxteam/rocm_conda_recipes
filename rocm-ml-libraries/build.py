import os
from pathlib import Path
from argparse import ArgumentParser
from subprocess import check_output, check_call
import shutil


rocblas_files_to_delete = [
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

files_to_patch = [
    {
        'file': os.path.join('hipfft', 'lib', 'cmake', 'hipfft', 'hipfft-targets.cmake'),
        'changes': [('/opt/rocm-5.1.0', '${_IMPORT_PREFIX}')]
    },
]


def patch_files():
    for info in files_to_patch:
        p = Path(os.environ['PREFIX'], info['file']).resolve()
        filedata = p.read_text()
        for change in info['changes']:
            filedata = filedata.replace(change[0], change[1])
        p.write_text(filedata)


def archive_rocblas_binaries(args):
    cmd = [
        "sudo",
        "zip",
        "-rj",
        # TODO: fix zip duct tape by making separate rocblas dependency
        "/opt/rocm-{}/rocblas/lib/library/mllibrary.zip".format(args.rocmrelease),
        "/opt/rocm-{}/rocblas/lib/library".format(args.rocmrelease),
    ]
    check_call(cmd)
    for ftd in rocblas_files_to_delete:
        cmd = [
            "sudo",
            "rm",
            "/opt/rocm-{}/rocblas/lib/library/{}".format(args.rocmrelease, ftd),
        ]
        check_call(cmd)


def remove_zip(args):
    cmd = [
            "sudo",
            "rm",
            "/opt/rocm-{}/rocblas/lib/library/mllibrary.zip".format(args.rocmrelease)
        ]
    check_call(cmd)


def copy(args):
    shutil.copytree(f'/opt/rocm-{args.rocmrelease}/', os.environ['PREFIX'], symlinks=True, dirs_exist_ok=True)


def install_rocm(args):
    cmd = [
            "sudo",
            "amdgpu-install",
            "-y",
            "--usecase=mllib",
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
    archive_rocblas_binaries(args)
    copy(args)
    remove_zip(args)
    patch_files()
    uninstall_rocm(args)


if __name__ == "__main__":
    main()