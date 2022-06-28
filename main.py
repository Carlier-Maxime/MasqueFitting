import os
import shutil
import sys
import numpy as np

sys.path.append('flame-fitting')
from fitting.landmarks import load_picked_points


def run():
    if not os.path.exists('flame-fitting/models/generic_model.pkl'):
        print("Télécharger le  flame model ! (plus d'information dans README.md)")
    files = next(os.walk('input'), (None, None, []))[2]
    nbScan = 0
    nbNoLmk = 0
    os.chdir('input')
    for file in files:
        if not file.endswith('.obj'):
            continue
        nbScan += 1
        base_name = file.split('.obj')[0]
        if os.path.exists(base_name + '.pp'):
            array = load_picked_points(base_name + ".pp")
            np.save("../flame-fitting/data/scan_lmks.npy", array)
        elif os.path.exists(base_name + '.txt'):
            print('format txt coming soon')
            exit(0)
        else:
            nbNoLmk += 1
            print("Le scan 3D '" + file + " n'as pas de fichier landmark ! (le nom de ce fichier doit-être "
                  + base_name + ".txt ou " + base_name + ".pp)")
            continue
        shutil.copyfile(base_name+".obj", "../flame-fitting/data/scan.obj")

    if nbScan == 0:
        print("Aucun scan fournie.")
    else:
        if nbScan != nbNoLmk:
            print(nbScan - nbNoLmk, "scan sur", nbScan, "ont été traité avec succès !")
        if nbNoLmk > 0:
            print(nbNoLmk, "scan sur", nbScan, "n'ont pas de fichier landmark ! Ils ont donc pas pu être traité.")


if __name__ == '__main__':
    run()
