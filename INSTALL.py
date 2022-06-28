import os

os.system('pip install -r requirements.txt')
os.chdir('flame-fitting/sbody/alignment/mesh_distance')
os.system('git clone https://gitlab.com/libeigen/eigen.git')
os.system('make')
os.chdir('../../../')

if bool(input('Do you want to delete the installation file ? (0|1) : ')):
    os.remove('INSTALL.py')
