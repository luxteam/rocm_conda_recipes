import os
import subprocess
import requests
import urllib.parse as urlparse

from tqdm import tqdm

def download_from_url(url, dst):
    """
    @param: url to download file
    @param: dst place to put the file
    """
    file_size = int(requests.head(url).headers["Content-Length"])
    if os.path.exists(dst):
        first_byte = os.path.getsize(dst)
    else:
        first_byte = 0
    if first_byte >= file_size:
        return file_size
    header = {"Range": "bytes=%s-%s" % (first_byte, file_size)}
    pbar = tqdm(
        total=file_size, initial=first_byte,
        unit='B', unit_scale=True, desc=url.split('/')[-1])
    req = requests.get(url, headers=header, stream=True)
    with(open(dst, 'ab')) as f:
        for chunk in req.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                pbar.update(1024)
        pbar.close()
    return file_size

config = {}
# TODO: remove default value later
config['src_dir'] = os.environ['SRC_DIR']
config['base_url'] = 'https://repo.radeon.com/rocm/apt/4.2/pool/main/'
config['rocm_packages'] = [
    'c/comgr/comgr_2.0.0.40200-21_amd64.deb',
    'r/rock-dkms/rock-dkms-firmware_4.2-21_all.deb',
    'r/rock-dkms/rock-dkms_4.2-21_all.deb',
    'r/rocm-dkms/rocm-dkms_4.2.0.40200-21_amd64.deb',
    'r/rocm-clang-ocl/rocm-clang-ocl_0.5.0.40200-21_amd64.deb',
    'r/rocm-cmake/rocm-cmake_0.4.0.40200-21_amd64.deb',
    'r/rocm-dbgapi/rocm-dbgapi_0.46.0.40200-21_amd64.deb',
    'r/rocm-debug-agent/rocm-debug-agent_2.0.1.40200-21_amd64.deb',
    'r/rocm-dev/rocm-dev_4.2.0.40200-21_amd64.deb',
    'r/rocm-device-libs/rocm-device-libs_1.0.0.40200-21_amd64.deb',
    'r/rocm-gdb/rocm-gdb_10.1.40200-21_amd64.deb',
    'r/rocm-smi-lib/rocm-smi-lib_2.8.0.40200-21_amd64.deb',
    'r/rocm-opencl/rocm-opencl_2.0.0.40200-21_amd64.deb',
    'r/rocm-opencl-dev/rocm-opencl-dev_2.0.0.40200-21_amd64.deb',
    'r/rocm-utils/rocm-utils_4.2.0.40200-21_amd64.deb',
    'r/rocminfo/rocminfo_1.0.0.40200-21_amd64.deb',
    'r/rocprofiler-dev/rocprofiler-dev_1.0.0.40200-21_amd64.deb',
    'r/roctracer-dev/roctracer-dev_1.0.0.40200-21_amd64.deb',
    'h/hip-rocclr/hip-rocclr_4.2.21155.5900.40200-21_amd64.deb',
    'h/hip-base/hip-base_4.2.21155.5900.40200-21_amd64.deb',
    'h/hip-doc/hip-doc_4.2.21155.5900.40200-21_amd64.deb',
    'h/hip-samples/hip-samples_4.2.21155.5900.40200-21_amd64.deb',
    'h/hsa-amd-aqlprofile/hsa-amd-aqlprofile_1.0.0.40200-21_amd64.deb',
    'h/hsakmt-roct/hsakmt-roct_20210315.0.7.40200-21_amd64.deb',
    'h/hsa-rocr-dev/hsa-rocr-dev_1.3.0.40200-21_amd64.deb',
    'l/llvm-amdgpu/llvm-amdgpu_12.0.0.21161.40200_amd64.deb',
    'o/openmp-extras/openmp-extras_12.42.0.40200-21_amd64.deb',
]


def download_packages(cfg):
    for package_url in cfg['rocm_packages']:
        dl_dst = os.path.join(cfg['src_dir'], os.path.basename(package_url))
        dl_src = urlparse.urljoin(cfg['base_url'], package_url)
        download_from_url(dl_src, dl_dst)


def extract_packages(cfg):
	script_path = os.path.join(cfg['src_dir'], 'extract_packages.sh')
	subprocess.call(['bash', script_path, cfg['src_dir'], os.environ['PREFIX']])
	

def main():
    download_packages(config)
    extract_packages(config)


if __name__ == "__main__":
    main()