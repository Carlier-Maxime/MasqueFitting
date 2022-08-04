def gen_packages_md():
    lines = []
    color = ['red', 'brown', 'orange', 'bisque', 'yellow', 'gold', 'green', 'olivedrab', 'limegreen', 'aquamarine', 'steelblue', 'teal', 'skyblue', 'blue', 'blueviolet']
    links = {
        "chumpy": "https://github.com/mattloper/chumpy",
        "colorama": "https://github.com/tartley/colorama",
        "Cython": "https://github.com/cython/cython",
        "face--alignment": "https://github.com/1adrianb/face-alignment",
        "imageio": "https://github.com/imageio/imageio",
        "llvmlite": "https://github.com/numba/llvmlite",
        "networkx": "https://github.com/networkx/networkx",
        "numba": "https://github.com/numba/numba",
        "numpy": "https://github.com/numpy/numpy",
        "opencv--python": "https://github.com/opencv/opencv-python",
        "packaging": "https://github.com/pypa/packaging",
        "Panda3D": "https://github.com/panda3d/panda3d",
        "Pillow": "https://github.com/python-pillow/Pillow",
        "psbody--mesh": "https://github.com/MPI-IS/mesh",
        "PyOpenGL": "https://github.com/mcfletch/pyopengl",
        "pyparsing": "https://github.com/pyparsing/pyparsing",
        "PyWavelets": "https://github.com/PyWavelets/pywt",
        "PyYAML": "https://github.com/yaml/pyyaml",
        "pyzmq": "https://github.com/zeromq/pyzmq",
        "scikit--image": "https://github.com/scikit-image/scikit-image",
        "scipy": "https://github.com/scipy/scipy",
        "six": "https://github.com/benjaminp/six",
        "tifffile": "https://github.com/cgohlke/tifffile",
        "torch": "https://github.com/pytorch/pytorch",
        "tqdm": "https://github.com/tqdm/tqdm",
        "trimesh": "https://github.com/mikedh/trimesh",
        "typing_extensions": "https://github.com/python/typing_extensions",
        "Werkzeug": "https://github.com/pallets/werkzeug",
        "zmq": "https://github.com/zeromq/pyzmq"
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
            img = f'![{package[0]} : {package[1]}](https://img.shields.io/badge/{package[0]}-{package[1]}-{color[n % len(color)]})'
            if package[0] in links and links[package[0]] != "":
                lines.append(f"[{img}]({links[package[0]]})\n")
            else:
                lines.append(img+"\n")
            n += 1

    with open("packages.md", "w") as f:
        for line in lines:
            f.write(line)
