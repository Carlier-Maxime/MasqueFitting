import logging as log
import os
import shutil
import sys

import numpy as np
import trimesh

import get_landmarks
import util
from config import get_config
from flameFitting.fitting.landmarks import load_picked_points

def run():
    print("Load config")
    config = get_config()
    if config.output_format not in ['npy', 'txt', 'pp', 'obj', 'stl']:
        log.error("The format of output file is unknown or not supported.")
        exit(1)
    if not os.path.exists('flameFitting/models/generic_model.pkl'):
        log.error("Download the flame model ! (More information in README.md)")
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

    print("Browse file of input folder..")
    for file in files:
        if not in_input:
            os.chdir('input')
            in_input = True
        if not file.endswith('.obj') and not file.endswith(".stl"):
            continue
        nbScan += 1
        print(f"Treatment of {file} (scan N°{nbScan})")
        base_name = file.split('.obj')[0].split(".stl")[0]

        # generate normal, remove color and texture, save to obj format
        print("Prepare 3D file")
        mesh = trimesh.load_mesh(file)
        normals = mesh.vertex_normals
        with open("../tmp/" + base_name + ".obj", "w") as f:
            f.write(trimesh.exchange.obj.export_obj(mesh, True, False, False))

        if config.auto_lmk:
            print("Auto generate the 51 landmarks..")
            os.chdir("..")
            if config.input_flame_visage:
                get_landmarks.run(f"tmp/{base_name}.obj", 0.77, -0.18, 0.86, 90, -45, 0, 26.3201, 17, 0, 0, 10, 90, -45, 0)
            else:
                get_landmarks.run(f"tmp/{base_name}.obj", config.panda3d_camera_x, config.panda3d_camera_y,
                                  config.panda3d_camera_z, config.panda3d_camera_h, config.panda3d_camera_p,
                                  config.panda3d_camera_r, config.panda3d_fov_i, config.panda3d_fov_j,
                                  config.panda3d_light_x, config.panda3d_light_y, config.panda3d_light_z,
                                  config.panda3d_light_h, config.panda3d_light_p, config.panda3d_light_r)
            os.chdir('tmp')
            print("Generation landmarks, finish.")
        print("Prepare flameFitting")
        if os.path.exists(base_name + '.pp'):
            array = load_picked_points(base_name + ".pp")
            np.save("../flameFitting/data/scan_lmks.npy", array)
        elif os.path.exists(base_name + '.txt'):
            array = []
            with open(base_name+".txt", "r") as f:
                while True:
                    line = f.readline()
                    if line == "":
                        break
                    line = line.split(',')
                    array.append([float(line[0]), float(line[1]), float(line[2])])
            np.save("../flameFitting/data/scan_lmks.npy", array)
        else:
            nbNoLmk += 1
            log.warning(f"The 3D scan '{file}' not landmark file ! (the name of file must be {base_name}.txt or {base_name}.pp)")
            continue
        os.chdir("../tmp")
        shutil.copyfile(base_name + ".obj", "../flameFitting/data/scan.obj")
        os.chdir('..')
        sys.path.append(os.path.abspath('flameFitting'))
        os.chdir('flameFitting')
        in_input = False
        import fit_scan
        print("Start flameFitting")
        fit_scan.run_fitting()
        print("flameFitting finish.")
        print("Obtain 3D markers of model FLAME fitter")
        mesh = trimesh.load_mesh("output/fit_scan_result.obj")
        vertices, triangles = mesh.vertices, mesh.faces
        points = util.read_all_index_opti_tri(vertices, triangles, markers)
        print("Transform 3D marker in index correspondant of mask resize")
        mesh = trimesh.load_mesh('output/scan_scaled.obj')
        vertices, triangles = mesh.vertices, mesh.faces
        indexs = util.get_index_for_match_points(vertices, triangles, points)
        print("Interpret index on start mask")
        os.chdir('..')
        mesh = trimesh.load_mesh("tmp/" + base_name + ".obj")
        vertices, triangles = mesh.vertices, mesh.faces
        points = util.read_all_index_opti_tri(vertices, triangles, indexs)
        print("Save 3D marker obtained")
        util.save_points(points, "output/"+base_name, config.output_format, config.radius, mesh, config.blender_path)
    if nbScan == 0:
        log.warning("None scan given.")
    else:
        if nbScan != nbNoLmk:
            print(nbScan - nbNoLmk, "scan on", nbScan, "have been successfully treated !")
        if nbNoLmk > 0:
            log.warning(f"{nbNoLmk} scan on {nbScan} not have landmark file ! They therefore could not be treated.")


if __name__ == '__main__':
    run()
