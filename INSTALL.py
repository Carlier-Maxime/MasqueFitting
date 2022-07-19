import os

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
