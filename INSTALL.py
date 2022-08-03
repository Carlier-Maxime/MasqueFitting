import os
from sys import platform
from tqdm import tqdm
import requests
import shutil

if platform == "win32":
    print("Install for Windows..")
    print("Install python package")
    os.system("python -m venv venv")
    pip = os.path.abspath("venv/Scripts/pip")
    python = os.path.abspath("venv/Scripts/python")
    os.system(f'{python} -m pip install --upgrade pip')
    os.system(f'{pip} install -r requirements_windows.txt')
    with open("venv/Lib/site-packages/numba/__init__.py", "r") as f:
        lines = f.readlines()
    with open("venv/Lib/site-packages/numba/__init__.py", "w") as f:
        for number, line in enumerate(lines):
            if number not in [144, 145]:
                f.write(line)
    os.system(f"{pip} install -U numpy")
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
    os.rename(f"boost_{boost_version.replace('.','_')}", "boost")
    os.chdir("boost")
    print("Install boost")
    os.system("bootstrap")
    os.system("b2")
    os.chdir("..")
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
    os.rename("mesh-fix-MSVC_compilation", "psbody-mesh")
    os.chdir("psbody-mesh")
    print("Install psbody-mesh")
    os.system(f"{pip} install --no-deps --install-option=\"--boost-location=../boost\" --verbose --no-cache-dir .")
    print("Download eigen")
    os.chdir('../flameFitting/sbody/alignment/mesh_distance')
    os.system('git clone https://gitlab.com/libeigen/eigen.git')
    print("Install eigen")
    os.system(f"{python} setup.py build_ext --inplace")
    os.chdir('../../../..')
    print("Fix CRLF / LF problem")
    os.rename("flameFitting/models/flame_static_embedding.pkl",
              "flameFitting/models/flame_static_embedding_CRLF.pkl")
    os.rename("flameFitting/models/flame_static_embedding_LF.pkl",
              "flameFitting/models/flame_static_embedding.pkl")
    print("Install finish.")

else:
    os.system('python -m venv venv')
    os.system('pip install -r requirements.txt')
    os.system("pip install numpy==1.22 --target lmkDetection/numpy_1.22")
    os.system("pip install -U numpy")
    os.chdir('flameFitting/sbody/alignment/mesh_distance')
    os.system('git clone https://gitlab.com/libeigen/eigen.git')
    os.system('make')
    os.chdir('../../../..')

if bool(int(input("Veux tu supprimer le fichier d'installation ? (0|1) : "))):
    os.remove('INSTALL.py')
