import os
import shutil
import sys
import numpy as np
import read3D

sys.path.append('flame-fitting')
from fit_scan import run_fitting
from fitting.landmarks import load_picked_points


def get_index_for_match_points(vertices, faces, points, verbose=False, triangle_optimize=True, pas_tri=1000):
    """
    return: list index of index matching points.
    """
    assert len(vertices) > 0

    list_index = []
    no_tri = 0
    for ind in range(len(points)):
        if verbose:
            print(ind, "/", len(points) - 1, "points")
        p = points[ind]
        index = -1
        dist = -1
        v = []
        for i in range(len(vertices)):
            v = vertices[i]
            d = np.sqrt((v[0] - p[0]) ** 2 + (v[1] - p[1]) ** 2 + (v[2] - p[2]) ** 2)
            if dist == -1 or d < dist:
                index = i
                dist = d
        if triangle_optimize:
            index_triangles = get_index_triangles_match_vertex(faces, index)
            triangles = np.array(faces)[index_triangles]
            triangles = np.array(vertices)[triangles]
            vectors = get_vector_for_point(triangles, vertices[index])
            ind_vect = -1
            percentage = [0, 0]
            dist2 = dist
            for i in range(len(vectors)):
                vect = np.array(vectors[i]) / pas_tri
                perc = []
                distance = dist
                vert = vertices[index]
                for j in range(len(vect)):
                    pas = 0
                    for k in range(1, pas_tri):
                        v = vert + vect[j] * k
                        d = np.sqrt((v[0] - p[0]) ** 2 + (v[1] - p[1]) ** 2 + (v[2] - p[2]) ** 2)
                        if d <= distance:
                            pas = k
                            distance = d
                        else:
                            break
                    perc.append(pas / pas_tri)
                    vert = v
                if distance < dist2:
                    dist2 = distance
                    ind_vect = i
                    percentage = perc
            if ind_vect == -1:
                ind_tri = -1
                no_tri += 1
            else:
                ind_tri = index_triangles[ind_vect]
            list_index.append([index, ind_tri, percentage[0], percentage[1]])
        else:
            list_index.append(index)
    print(no_tri, "/", len(points), " points no need triangles !")
    return list_index


def get_index_triangles_match_vertex(triangles, index_point):
    faces = []
    for i in range(len(triangles)):
        if index_point in triangles[i]:
            faces.append(i)
    return faces


def get_vector_for_point(triangles, p):
    """
    input:
        - triangles : triangle array => triangle = coo triangle [x,y,z]
        - p : coo point
    """
    vectors = []
    for triangle in triangles:
        t = [0, 0, 0]
        ind = []
        for i in range(3):
            if p[0] == triangle[i][0] and p[1] == triangle[i][1] and p[2] == triangle[i][2]:
                t[0] = triangle[i]
            else:
                ind.append(i)
        if len(ind) > 2:
            print("Error in getVectoForPoint in util.py ! (verify your point is vertex of triangles)")
            exit(1)
        t[1] = triangle[ind[0]]
        t[2] = triangle[ind[1]]

        v = []
        for i in range(1, 3):
            v.append([t[i][0] - p[0], t[i][1] - p[1], t[i][2] - p[2]])
        vectors.append(v)
    return vectors


def read_index_opti_tri(vertices, faces, index_opti_tri):
    p = vertices[int(index_opti_tri[0])]
    if index_opti_tri[1] != -1:
        tri = np.array(vertices)[faces[int(index_opti_tri[1])]]
        vectors = np.array(get_vector_for_point([tri], p)[0])
        p = p + vectors[0] * index_opti_tri[2]
        p = p + vectors[1] * index_opti_tri[3]
    return p


def read_all_index_opti_tri(vertices, faces, indexs_opti_tri):
    points = []
    for indexOptiTri in indexs_opti_tri:
        points.append(read_index_opti_tri(vertices, faces, indexOptiTri))
    return points


def run():
    if not os.path.exists('flame-fitting/models/generic_model.pkl'):
        print("Télécharger le  flame model ! (plus d'information dans README.md)")
    markers = np.load("markers.npy")
    files = next(os.walk('input'), (None, None, []))[2]
    nbScan = 0
    nbNoLmk = 0
    if not os.path.exists('output'):
        os.mkdir('output')
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
        shutil.copyfile(base_name + ".obj", "../flame-fitting/data/scan.obj")
        os.chdir('../flame-fitting')
        run_fitting()
        vertices, triangles = read3D.read("output/fit_scan_result.obj")
        points = read_all_index_opti_tri(vertices, triangles, markers)
        vertices, triangles = read3D.read('output/scan_scaled.obj')
        indexs = get_index_for_match_points(vertices, triangles, points)
        os.chdir('..')
        vertices, triangles = read3D.read('input/'+base_name+".obj")
        points = read_all_index_opti_tri(vertices, triangles, indexs)
        np.save("output/"+base_name+".npy", points)
    if nbScan == 0:
        print("Aucun scan fournie.")
    else:
        if nbScan != nbNoLmk:
            print(nbScan - nbNoLmk, "scan sur", nbScan, "ont été traité avec succès !")
        if nbNoLmk > 0:
            print(nbNoLmk, "scan sur", nbScan, "n'ont pas de fichier landmark ! Ils ont donc pas pu être traité.")


if __name__ == '__main__':
    run()
