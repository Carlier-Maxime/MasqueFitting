from datetime import datetime

import numpy as np


def save_points(points, file_base_name, format="npy"):
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
        with open(file_base_name + ".obj", "w") as f:
            for p in points:
                f.write(f'v {p[0]} {p[1]} {p[2]}\n')
