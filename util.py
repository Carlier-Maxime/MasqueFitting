from datetime import datetime
from distutils.spawn import find_executable

import numpy as np
import madcad
import trimesh


def save_points(points, file_base_name, format="npy", radius=2, mask=None):
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
        spheres = madcad.uvsphere(points[0], radius)
        for i in range(1, len(points)):
            sm = madcad.uvsphere(points[i], radius)
            nbv = len(spheres.points)
            spheres.points += sm.points
            for face in sm.faces:
                spheres.faces += [face + nbv]
        if format == "stl":
            madcad.io.write(spheres, file_base_name + ".stl")
        elif format == "obj":
            with open(file_base_name + ".obj", "w") as f:
                for p in spheres.points:
                    f.write(f'v {p[0]} {p[1]} {p[2]}\n')
                for face in spheres.faces:
                    f.write(f'f {face[0]} {face[1]} {face[2]}\n')

def simply_obj(file):
    """
    Supress Color, normal, comment in obj file

    Parameters
    ----------
    file

    Returns
    -------

    """
    content = ""
    with open(file, "r") as f:
        line = "start"
        while line != "":
            line = f.readline()
            if line.startswith("v "):
                line = line.split(" ")
                content += f'v {line[1]} {line[2]} {line[3]}'
                if len(line) > 4:
                    content += '\n'
            elif line.startswith("f "):
                line = line.split(" ")
                content += f'f {line[1].split("/")[0]} {line[2].split("/")[0]} {line[3].split("/")[0]}\n'
    with open(file, "w") as f:
        f.write(content)


def get_normal(vertices, triangles):
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


def get_normal_core(normal, tri_normal, triangles, ntri):
    for i in range(ntri):
        tri_p0_ind = triangles[i][0]
        tri_p1_ind = triangles[i][1]
        tri_p2_ind = triangles[i][2]

        for j in range(3):
            normal[tri_p0_ind][j] = normal[tri_p0_ind][j] + tri_normal[i][j]
            normal[tri_p1_ind][j] = normal[tri_p1_ind][j] + tri_normal[i][j]
            normal[tri_p2_ind][j] = normal[tri_p2_ind][j] + tri_normal[i][j]