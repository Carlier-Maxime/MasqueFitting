import os
from sys import platform
from tqdm import tqdm
import requests
import shutil

if platform == "win32":
    print("Install for Windows..")
    print("Install python package")
    os.system("python -m venv venv")
    os.system('pip install -r requirements_windows.txt')
    os.system("pip install numpy==1.22 --target lmk-detection/numpy_1.22")
    os.system("pip install -U numpy")
    print("Download boost")
    boost_version = "1.79.0"
    url = f"https://boostorg.jfrog.io/artifactory/main/release/{boost_version}/source/boost_{boost_version.replace('.','_')}.zip"
    resp = requests.get(url, stream=True)
    total = int(resp.headers.get('content-length', 0))
    fname = "boost.zip"
    with open(fname, "wb") as file, tqdm(desc=fname, total=total, unit='iB', unit_scale=True, unit_divisor=1024) as bar:
        for data in resp.iter_content(chunk_size=1024):
            size = file.write(data)
            bar.update(size)
    print("Unzip boost")
    shutil.unpack_archive("boost.zip")
    os.remove("boost.zip")
    os.chdir(f"boost_{boost_version.replace('.','_')}")
    print("Install boost")
    os.system("./bootstrap")
    os.system("./b2")
    print("Download psbody-mesh")
    url = "https://github.com/johnbanq/mesh/archive/refs/heads/fix/MSVC_compilation.zip"
    resp = requests.get(url, stream=True)
    total = int(resp.headers.get('content-length', 0))
    fname = "psbody-mesh.zip"
    with open(fname, "wb") as file, tqdm(desc=fname, total=total, unit='iB', unit_scale=True, unit_divisor=1024) as bar:
        for data in resp.iter_content(chunk_size=1024):
            size = file.write(data)
            bar.update(size)
    print("Unzip psbody-mesh")
    shutil.unpack_archive("psbody-mesh.zip")
    os.remove("psbody-mesh.zip")
    os.chdir("psbody-mesh")
    print("Install psbody-mesh")
    os.system("pip install --no-deps --install-option=\"--boost-location=../boost\" --verbose --no-cache-dir .")
    print("Download eigen")
    os.chdir('../flame-fitting/sbody/alignment/mesh_distance')
    os.system('git clone https://gitlab.com/libeigen/eigen.git')
    print("Install eigen")
    os.system("python setup.py build_ext --inplace")
    os.chdir('../../../..')
    print("Install finish.")

else:
    os.system('python -m venv venv')
    os.system('pip install -r requirements.txt')
    os.system("pip install numpy==1.22 --target lmk-detection/numpy_1.22")
    os.system("pip install -U numpy")
    os.chdir('flame-fitting/sbody/alignment/mesh_distance')
    os.system('git clone https://gitlab.com/libeigen/eigen.git')
    os.system('make')
    os.chdir('../../../..')

if bool(int(input("Veux tu supprimer le fichier d'installation ? (0|1) : "))):
    os.remove('INSTALL.py')
