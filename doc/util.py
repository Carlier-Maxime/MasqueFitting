def gen_packages_md():
    lines = []
    color = ['red', 'brown', 'orange', 'bisque', 'yellow', 'gold', 'green', 'olivedrab', 'limegreen', 'aquamarine', 'steelblue', 'teal', 'skyblue', 'blue', 'blueviolet']
    links = {
        "chumpy": "",
        "colorama": "",
        "Cython": "",
        "face-alignment": "",
        "imageio": "",
        "llvmlite": "",
        "networkx": "",
        "numba": "",
        "numpy": "",
        "opencv-python": "",
        "packaging": "",
        "Panda3D": "",
        "Pillow": "",
        "psbody-mesh": "",
        "PyOpenGL": "",
        "pyparsing": "",
        "PyWavelets": "",
        "PyYAML": "",
        "pyzmq": "",
        "scikit-image": "",
        "scipy": "",
        "six": "",
        "tifffile": "",
        "torch": "",
        "tqdm": "",
        "trimesh": "",
        "typing_extensions": "",
        "Werkzeug": "",
        "zmq": ""
    }
    with open("packages.txt", "r", encoding="UTF-16LE") as f:
        n = 0
        while f.readable():
            package = f.readline()
            if package == "":
                break
            package = package.split('==')
            sp = package[0].split("\ufeff")
            package[0] = sp[1] if len(sp) > 1 else sp[0]
            package[0] = package[0].replace('-', '--')
            package[1] = package[1].split('\n')[0]
            img = f'![{package[0]} : {package[1]}](https://img.shields.io/badge/{package[0]}-{package[1]}-{color[n % len(color)]})\n'
            if package[0] in links and links[package[0]] != "":
                lines.append(f"[{img}]({links[package[0]]})")
            else:
                lines.append(img)
            n += 1

    with open("packages.md", "w") as f:
        for line in lines:
            f.write(line)
