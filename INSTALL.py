import os

os.system('pip install -r requirements.txt')
os.chdir('flame-fitting/sbody/alignment/mesh_distance')
os.system('git clone https://gitlab.com/libeigen/eigen.git')
os.system('make')
os.chdir('../../../..')

if bool(input("Veux tu supprimer le fichier d'installation ? (0|1) : ")):
    os.remove('INSTALL.py')
