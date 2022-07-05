import os
import shutil
import sys
import numpy as np
import read3D

from config import get_config
from datetime import datetime
sys.path.append('flame-fitting')
from fit_scan import run_fitting
from fitting.landmarks import load_picked_points


def get_index_for_match_points(vertices, faces, points, verbose=False, triangle_optimize=True, pas_tri=1000):
    """
    allows you to obtain the clues that best correspond to the points provided.
    it can be vertex indexes or more complex indexes depending on the triangle_optimize value.
    Parameters:
        - vertices: the array of all vertex (one vertex is a point represented in an array : [x, y, z])
        - faces: the array of all face / triangle (one face is an array containing 3 index of vertex : [i, j, k])
        - points: the array of all point (one point is represented in an array : [x, y, z])
        - verbose: is a boolean allowing to choose to display or not the progress
        - triangle_optimize: is a boolean allowing to choose whether or not to use the triangles to optimize the index.
            Optimization with triangles returns indexes which are arrays containing different information:
            the format of index : [index_vertex, index_triangle, percentage_vector_1, percentage_vector_2]
            format detail :
                - index_vertex: index of vertex
                - index_triangle: index of triangle
                - percentage_vector_1: percentage of vector one
                - percentage_vector_2: percentage of vector two
            vector 1 and 2 are calculated using as origin the vertex of index index_vertex and as
            destination one of the other points of the triangle.
            the destination point is obtained with respect to the order of the vertices in the triangle,
            by not tacking the original vertices. the list of possibility :
            - [origin, dest1, dest2]
            - [dest1, origin, dest2]
            - [dest1, dest2, origin]
        - pas_tri : is an integer corresponding to the progress step for the vectors. (1000 == 0.1% of vector per step)
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
    if verbose:
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
    config = get_config()
    if config.output_format not in ['npy', 'txt', 'pp', 'obj']:
        print("Le format du fichier de sortie est inconnue ou non pris en charge.")
        exit(0)
    if not os.path.exists('flame-fitting/models/generic_model.pkl'):
        print("Télécharger le flame model ! (plus d'information dans README.md)")
        exit(0)
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
        if config.output_format == "npy":
            np.save("output/"+base_name+".npy", points)
        elif config.output_format == "txt":
            with open("output/"+base_name+".txt", "w") as f:
                for p in points:
                    f.write(f'{p[0]},{p[1]},{p[2]}\n')
        elif config.output_format == "pp":
            with open("output/"+base_name+".pp", "w") as f:
                t = datetime.now()
                f.write(
                    '<!DOCTYPE PickedPoints>\n' +
                    '<PickedPoints>\n' +
                    ' <DocumentData>\n' +
                    f'  <DateTime time="{t.strftime("%H:%M:%S")}" date="{t.strftime("%Y-%m-%d")}"/>\n' +
                    f'  <DataFileName name="{base_name}.obj"/>\n' +
                    ' </DocumentData>\n'
                )
                for i in range(len(points)):
                    p = points[i]
                    f.write(f' <point y="{p[1]}" z="{p[2]}" active="1" name="{i}" x="{p[0]}"/>\n')
                f.write('</PickedPoints>\n')
        elif config.output_format == "obj":
            with open("output/"+base_name+".obj", "w") as f:
                for p in points:
                    f.write(f'v {p[0]} {p[1]} {p[2]}\n')
    if nbScan == 0:
        print("Aucun scan fournie.")
    else:
        if nbScan != nbNoLmk:
            print(nbScan - nbNoLmk, "scan sur", nbScan, "ont été traité avec succès !")
        if nbNoLmk > 0:
            print(nbNoLmk, "scan sur", nbScan, "n'ont pas de fichier landmark ! Ils ont donc pas pu être traité.")


if __name__ == '__main__':
    run()
