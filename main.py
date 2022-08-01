import os
import shutil
import sys
import numpy as np
import trimesh
import logging as log

import util

from config import get_config

sys.path.append('flame-fitting')
from fitting.landmarks import load_picked_points


def run():
    print("chargement de la configuration")
    config = get_config()
    pyv = config.python_version
    if config.output_format not in ['npy', 'txt', 'pp', 'obj', 'stl']:
        log.error("Le format du fichier de sortie est inconnue ou non pris en charge.")
        exit(1)
    if not os.path.exists('flame-fitting/models/generic_model.pkl'):
        log.error("Télécharger le flame model ! (plus d'information dans README.md)")
        exit(1)
    markers = np.load("markers.npy")
    files = next(os.walk('input'), (None, None, []))[2]
    nbScan = 0
    nbNoLmk = 0
    if not os.path.exists('output'):
        os.mkdir('output')
    if not os.path.exists('tmp'):
        os.mkdir('tmp')
    in_input = False

    print("Parcourir les fichier du dossier input..")
    for file in files:
        if not in_input:
            os.chdir('input')
            in_input = True
        if not file.endswith('.obj') and not file.endswith(".stl"):
            continue
        nbScan += 1
        print(f"traitement de {file} (scan N°{nbScan})")
        base_name = file.split('.obj')[0].split(".stl")[0]

        # generate normal, remove color and texture, save to obj format
        print("Préparation du fichier 3D")
        mesh = trimesh.load_mesh(file)
        normals = mesh.vertex_normals
        with open("../tmp/" + base_name + ".obj", "w") as f:
            f.write(trimesh.exchange.obj.export_obj(mesh, True, False, False))

        if config.auto_lmk:
            print("Génération automatiques des 51 landmarks..")
            os.chdir("..")
            os.system(f"python{pyv} get_landmarks.py tmp/{base_name}.obj {pyv}")
            os.chdir('tmp')
            print("génération des landmarks, terminée.")
        print("Préparation de flame-fitting")
        if os.path.exists(base_name + '.pp'):
            array = load_picked_points(base_name + ".pp")
            np.save("../flame-fitting/data/scan_lmks.npy", array)
        elif os.path.exists(base_name + '.txt'):
            array = []
            with open(base_name+".txt", "r") as f:
                while True:
                    line = f.readline()
                    if line == "":
                        break
                    line = line.split(',')
                    array.append([float(line[0]), float(line[1]), float(line[2])])
            np.save("../flame-fitting/data/scan_lmks.npy", array)
        else:
            nbNoLmk += 1
            log.warning("Le scan 3D '" + file + " n'as pas de fichier landmark ! (le nom de ce fichier doit-être "
                  + base_name + ".txt ou " + base_name + ".pp)")
            continue
        os.chdir("../tmp")
        shutil.copyfile(base_name + ".obj", "../flame-fitting/data/scan.obj")
        os.chdir('../flame-fitting')
        in_input = False
        print("lancement de flame-fitting")
        os.system(f'python{pyv} fit_scan.py')
        print("flame-fitting terminée.")
        print("récupération des markers 3D sur le model FLAME fitter")
        mesh = trimesh.load_mesh("output/fit_scan_result.obj")
        vertices, triangles = mesh.vertices, mesh.faces
        points = util.read_all_index_opti_tri(vertices, triangles, markers)
        print("transformation des marker 3D en index correspondant aux masque redimensionner")
        mesh = trimesh.load_mesh('output/scan_scaled.obj')
        vertices, triangles = mesh.vertices, mesh.faces
        indexs = util.get_index_for_match_points(vertices, triangles, points)
        print("Interprétation des index sur le masque de départ")
        os.chdir('..')
        mesh = trimesh.load_mesh("tmp/" + base_name + ".obj")
        vertices, triangles = mesh.vertices, mesh.faces
        points = util.read_all_index_opti_tri(vertices, triangles, indexs)
        print("Enregistrement des marker 3D obtenue")
        util.save_points(points, "output/"+base_name, config.output_format, config.radius, mesh, config.blender_path)
    if nbScan == 0:
        log.warning("Aucun scan fournie.")
    else:
        if nbScan != nbNoLmk:
            print(nbScan - nbNoLmk, "scan sur", nbScan, "ont été traité avec succès !")
        if nbNoLmk > 0:
            log.warning(f"{nbNoLmk} scan sur {nbScan} n'ont pas de fichier landmark ! Ils ont donc pas pu être traité.")


if __name__ == '__main__':
    run()
