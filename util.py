from datetime import datetime

import numpy as np
import trimesh


def save_points(points, file_base_name, format="npy", radius=2):
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
    elif format == "obj":
        sm = trimesh.creation.uv_sphere(radius=radius)
        tfs = np.tile(np.eye(4), (1, 1))
        nbVertice = 0
        with open(file_base_name + ".obj", "w") as f:
            for p in points:
                tfs[:3, 3] = p
                sphere = sm.copy()
                sphere.apply_transform(tfs)
                vertices = sphere.vertices
                faces = sphere.faces
                for v in vertices:
                    f.write(f'v {v[0]} {v[1]} {v[2]}\n')
                for face in faces:
                    f.write(f'f {face[0]+nbVertice} {face[1]+nbVertice} {face[2]+nbVertice}\n')
                nbVertice += len(vertices)
