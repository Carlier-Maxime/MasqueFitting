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
