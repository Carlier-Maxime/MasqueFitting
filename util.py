import os
import sys
import shutil
from datetime import datetime
from distutils.spawn import find_executable

import numpy as np
import logging as log
import trimesh

sys.path.append('flame-fitting')
from fitting.landmarks import load_picked_points


def save_points(points: list, file_base_name: str, format: str = "npy", radius: float = 2, mask=None,
                blender_path: str = "./blender"):
    """
    Save 3d points to the specific format.
    Args:
        points (list): array of all 3d point
        file_base_name (str): file base name for the save
        format (str): format used for save
        radius (float): radius for the sphere represented 3d point
        mask: input 3d object, used for boolean difference why bool
        blender_path (str): path to blender, user for use blender for boolean difference
    Returns: None
    """
    if format == "npy":
        np.save(file_base_name + ".npy", points)
    elif format == "txt":
        with open(file_base_name + ".txt", "w") as f:
            for p in points:
                f.write(f'{p[0]},{p[1]},{p[2]}\n')
    elif format == "pp":
        with open(file_base_name + ".pp", "w") as f:
            t = datetime.now()
            f.write(
                '<!DOCTYPE PickedPoints>\n' +
                '<PickedPoints>\n' +
                ' <DocumentData>\n' +
                f'  <DateTime time="{t.strftime("%H:%M:%S")}" date="{t.strftime("%Y-%m-%d")}"/>\n' +
                f'  <DataFileName name="{file_base_name}.obj"/>\n' +
                ' </DocumentData>\n'
            )
            for i in range(len(points)):
                p = points[i]
                f.write(f' <point y="{p[1]}" z="{p[2]}" active="1" name="{i}" x="{p[0]}"/>\n')
            f.write('</PickedPoints>\n')
    elif format in ["obj", "stl"]:
        print("transformation des points en sphere")
        spheres = []
        for i in range(len(points)):
            sphere = trimesh.creation.uv_sphere(radius)
            sphere.vertices += points[i]
            spheres.append(sphere)

        print("différence boolean avec le masque d'origine")
        blender = trimesh.interfaces.blender
        blender._search_path += ';' + blender_path
        blender._blender_executable = find_executable('blender', path=blender._search_path)
        blender.exists = blender._blender_executable is not None
        diff = mask.difference(spheres)

        print("sauvegarde du résultat")
        if format == "stl":
            with open(file_base_name + ".stl", "wb") as f:
                f.write(trimesh.exchange.stl.export_stl(diff))
        elif format == "obj":
            with open(file_base_name + ".obj", "w") as f:
                f.write(trimesh.exchange.obj.export_obj(diff))


def simply_obj(file: str, color: bool = False, normal: bool = False, comment: bool = False):
    """
    Supress by default Color, normal, comment in obj file
    Args:
        file (str): file path for obj
        color (bool): keep the color or not
        normal (bool): keep the normal or not
        comment (bool): keep the comment or not
    Returns None
    """
    content = ""
    with open(file, "r") as f:
        line = "start"
        while line != "":
            line = f.readline()
            if line.startswith("v "):
                if not color:
                    line = line.split(" ")
                    content += f'v {line[1]} {line[2]} {line[3]}'
                    if len(line) > 4:
                        content += '\n'
                else:
                    content += line
            elif line.startswith("f "):
                if not normal:
                    line = line.split(" ")
                    content += f'f {line[1].split("/")[0]} {line[2].split("/")[0]} {line[3].split("/")[0]}\n'
                else:
                    content += line
            elif line.startswith("vn ") and normal:
                content += line
            elif comment:
                content += line

    with open(file, "w") as f:
        f.write(content)


def get_normal(vertices: list, triangles: list):
    """
    calculate normal direction in each vertex
    Args:
        vertices: [nver, 3]
        triangles: [ntri, 3]
    Returns:
        normal: [nver, 3]

    Source:
        https://github.com/YadiraF/face3d
    """
    pt0 = vertices[triangles[:, 0], :]  # [ntri, 3]
    pt1 = vertices[triangles[:, 1], :]  # [ntri, 3]
    pt2 = vertices[triangles[:, 2], :]  # [ntri, 3]
    tri_normal = np.cross(pt0 - pt1, pt0 - pt2)  # [ntri, 3]. normal of each triangle

    normal = np.zeros_like(vertices, dtype=np.float32).copy()  # [nver, 3]
    # for i in range(triangles.shape[0]):
    #     normal[triangles[i, 0], :] = normal[triangles[i, 0], :] + tri_normal[i, :]
    #     normal[triangles[i, 1], :] = normal[triangles[i, 1], :] + tri_normal[i, :]
    #     normal[triangles[i, 2], :] = normal[triangles[i, 2], :] + tri_normal[i, :]
    get_normal_core(normal, tri_normal.astype(np.float32).copy(), triangles.copy(), triangles.shape[0])

    # normalize to unit length
    mag = np.sum(normal ** 2, 1)  # [nver]
    zero_ind = (mag == 0)
    mag[zero_ind] = 1
    normal[zero_ind, 0] = np.ones((np.sum(zero_ind)))

    normal = normal / np.sqrt(mag[:, np.newaxis])

    return normal


def get_normal_core(normal: list, tri_normal: list, triangles: list, ntri: int):
    """
    Args:
        normal (list):
        tri_normal (list):
        triangles (list):
        ntri (int):
    """
    for i in range(ntri):
        tri_p0_ind = triangles[i][0]
        tri_p1_ind = triangles[i][1]
        tri_p2_ind = triangles[i][2]

        for j in range(3):
            normal[tri_p0_ind][j] = normal[tri_p0_ind][j] + tri_normal[i][j]
            normal[tri_p1_ind][j] = normal[tri_p1_ind][j] + tri_normal[i][j]
            normal[tri_p2_ind][j] = normal[tri_p2_ind][j] + tri_normal[i][j]


def change_markers(scan_path: str, pts_path: str, lmk_path: str = None, pyv: str = ""):
    """
    Change markers to the points given by file (pts_path).
    inverse main process for work.
    Args:
        scan_path (str): file path for the scan
        pts_path (str): file path for the points
        lmk_path (str): file path for the landmarks
        pyv (str): python version
    Returns: None
    """
    print("Vérification et chargement des points")
    if pts_path.endswith(".txt"):
        points = []
        with open(pts_path, "r") as f:
            while f.readable():
                line = f.readline()
                if line == "":
                    break
                line = line.split(",")[:3]
                p = [float(line[x].split('"')[1]) for x in range(3)]
                points.append(p)
        points = np.array(points)
    elif pts_path.endswith(".npy"):
        points = np.load(pts_path)
    else:
        log.warning("Format non prise en charge ! (le fichier pts doit-être au format txt ou npy)")
        exit(1)
    print("Préparation du fichier 3D")
    base_name = scan_path.split('.obj')[0].split(".stl")[0].split("/")
    base_name = base_name[len(base_name) - 1]
    mesh = trimesh.load_mesh(scan_path)
    normals = mesh.vertex_normals
    with open("tmp/" + base_name + ".obj", "w") as f:
        f.write(trimesh.exchange.obj.export_obj(mesh, True, False, False))

    if lmk_path is None:
        print("Génération automatiques des 51 landmarks..")
        os.system(f"python{pyv} get_landmarks.py tmp/{base_name}.obj {pyv}")
        lmk_path = f"tmp/{base_name}.pp"
        print("génération des landmarks, terminée.")

    print("Préparation de flame-fitting")
    if os.path.exists(lmk_path):
        array = load_picked_points(lmk_path)
        np.save("flame-fitting/data/scan_lmks.npy", array)
    else:
        log.warning("Le scan 3D '" + scan_path + " n'as pas de fichier landmark ! (le nom de ce fichier doit-être "
                    + base_name + ".txt ou " + base_name + ".pp)")
    shutil.copyfile(f"tmp/{base_name}.obj", "flame-fitting/data/scan.obj")
    print("lancement de flame-fitting")
    os.chdir("flame-fitting")
    os.system(f'python{pyv} fit_scan.py')
    os.chdir("..")
    print("flame-fitting terminée.")
    print("transformation des points en index")
    mesh = trimesh.load_mesh(f"tmp/{base_name}.obj")
    vertices, triangles = mesh.vertices, mesh.faces
    indexs = get_index_for_match_points(vertices, triangles, points, verbose=True)
    print("utilisation des index obtenue sur le masque redimenssionner")
    mesh = trimesh.load_mesh('flame-fitting/output/scan_scaled.obj')
    vertices, triangles = mesh.vertices, mesh.faces
    points = read_all_index_opti_tri(vertices, triangles, indexs)
    print("transformation des points en index pour le visage FLAME")
    mesh = trimesh.load_mesh("flame-fitting/output/fit_scan_result.obj")
    vertices, triangles = mesh.vertices, mesh.faces
    indexs = get_index_for_match_points(vertices, triangles, points)
    print("Enregistrement des indexs de marker obtenue")
    np.save("markers.npy", indexs)


def get_index_for_match_points(vertices: list, faces: list, points: list, verbose: bool = False,
                               triangle_optimize: bool = True, pas_tri: int = 1000):
    """
    allows you to obtain the clues that best correspond to the points provided.
    it can be vertex indexes or more complex indexes depending on the triangle_optimize value.
    Args:
        vertices (list): the array of all vertex (one vertex is a point represented in an array : [x, y, z])
        faces (list): the array of all face / triangle (one face is an array containing 3 index of vertex : [i, j, k])
        points (list): the array of all point (one point is represented in an array : [x, y, z])
        verbose (bool): is a boolean allowing to choose to display or not the progress
        triangle_optimize (bool):
            is a boolean allowing to choose whether or not to use the triangles to optimize the index.
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
        pas_tri (int): corresponding to the progress step for the vectors. (1000 == 0.1% of vector per step)
    Returns: list
        a list index of index matching points.
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


def get_index_triangles_match_vertex(triangles: list, index_vertex: list):
    """
    provides a list containing the indices of all triangles that contain the provided vertex
    Args:
        triangles (list): the array of all triangle / face (one triangle is an array containing 3 index of vertex : [i, j, k])
        index_vertex (int): the index of the vertex
    Returns: list
        a list containing the indices of all triangles that contain the provided vertex
    """
    faces = []
    for i in range(len(triangles)):
        if index_vertex in triangles[i]:
            faces.append(i)
    return faces


def get_vector_for_point(triangles: list, p: list):
    """
    Obtain vector for all triangle
    Args:
        triangles (list): triangle array => triangle = coo triangle [x,y,z]
        p (list): coo point
    Returns: all vectors based in the point for all triangles
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
            print("Error in getVectoForPoint in main.py ! (verify your point is vertex of triangles)")
            exit(1)
        t[1] = triangle[ind[0]]
        t[2] = triangle[ind[1]]

        v = []
        for i in range(1, 3):
            v.append([t[i][0] - p[0], t[i][1] - p[1], t[i][2] - p[2]])
        vectors.append(v)
    return vectors


def read_index_opti_tri(vertices: list, faces: list, index_opti_tri: list):
    """
    allows to retrieve the index point of the type :
    [index_vertex, index_triangle, percentage_vector_1, percentage_vector_2]
    Args:
        vertices :(list) the array of all vertex (one vertex is a point represented in an array : [x, y, z])
        faces (list): the array of all face / triangle (one face is an array containing 3 index of vertex : [i, j, k])
        index_opti_tri (list): a index of type : [index_vertex, index_triangle, percentage_vector_1, percentage_vector_2]
    Returns: point
        the point corresponding to the given index, point represented in an array : [x, y, z]
    """
    p = vertices[int(index_opti_tri[0])]
    if index_opti_tri[1] != -1:
        tri = np.array(vertices)[faces[int(index_opti_tri[1])]]
        vectors = np.array(get_vector_for_point([tri], p)[0])
        p = p + vectors[0] * index_opti_tri[2]
        p = p + vectors[1] * index_opti_tri[3]
    return p


def read_all_index_opti_tri(vertices: list, faces: list, indexes_opti_tri: list):
    """
    allows you to obtain all the points corresponding to the indexes opti tri provided
    Args:
        vertices (list): the array of all vertex (one vertex is a point represented in an array : [x, y, z])
        faces (list): the array of all face / triangle (one face is an array containing 3 index of vertex : [i, j, k])
        indexes_opti_tri (list): an array of all the opti tri indexes whose points you want.
            format of one index : [index_vertex, index_triangle, percentage_vector_1, percentage_vector_2]
    Returns: array
        the array of all point corresponding to the indexes provided. point represented in an array : [x, y, z]
    """
    points = []
    for indexOptiTri in indexes_opti_tri:
        points.append(read_index_opti_tri(vertices, faces, indexOptiTri))
    return points

