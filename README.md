# Fitting Mask

## Description

Mask Fitting allows you from a 3D scan to obtain the coordinates of the N markers corresponding to the points chosen on the flame face. (see [Use](#use)) <br>
By default they return you these 105 points: <br>
![Representation of the 105 points](doc/105points.gif) <br>
(This image is an illustration gif from [VisageGenerator](https://github.com/Carlier-Maxime/Visage-Generator)) <br>
Of course the coordinates of these 105 points are adapted in order to stick to the mask provided.


## Installation

### Prerequisites

To install / run Masque Fitting you must have:
- [python](https://www.python.org/) (to run python files including this program)
- [git](https://git-scm.com/) (to retrieve dependencies on git repositories ([psbody-mesh](https://github.com/MPI-IS/mesh) and [eigen ](https://gitlab.com/libeigen/eigen)))
- **g++** (not test if needed, but I guess it's needed to compile [eigen](https://gitlab.com/libeigen/eigen))
- [7zip](https://www.7-zip.org/download.html) or any other zip file manager to unzip the model file

### Recovery

Simply clone the project using git in the directory of your choice:
```
git clone https://github.com/Carlier-Maxime/MasqueFitting
```

### Dependencies

Open a terminal or a command prompt and run the installation file:
```
python INSTALL.py
```

If you want to install the dependencies manually, here is some information: <br>

- the list of required dependencies can be found in the requirements.txt file (with some exceptions)
- for psbody-mesh you will probably need to install [boost](https://www.boost.org/)
- To install psbody-mesh under Windows take the version present on this [repository](https://github.com/johnbanq/mesh/tree/fix/MSVC_compilation)
- most dependencies install with ```pip install <packagename>``` or run ```pip install -r requirements.txt``` which will install all required packages. on Windows run ```pip install -r requirements_windows.txt``` instead
- lmk-detection uses numba which requires an earlier version of numpy, but for the use made it works with a higher version. <br>
So go to the numba folder (venv/Lib/site-packages/numba on Windows if installing in a virtualenv python), in the file \_\_init\_\_.py and delete the 2 lines indicating the minimum version of numpy(L145-L146).
- by default you have to install eigen in flame-fitting/sbody/alignment/mesh-distance. <br>
For more information read the flame-fitting readme
- to install eigen on windows instead of running ```make``` run ```python setup.py build_ext --inplace```

hoping that this information for the manual installation will have been useful to you.
You can also look directly in the INSTALL.py file to better see the steps.

### Model

Download the flame model (preferably the 2020 one) [here](https://flame.is.tue.mpg.de/)
and unzip the archive obtained then place its content (the 3 model files) in flame-fitting/models.
(You can do it yourself as the installation.)

### Add-on

You can use the dots directly to turn them into a sphere and do the boolean difference on the input mask <br>
in order to directly obtain the input mask instead of a point cloud. (supported OBJ and STL save format) <br>
for this it is necessary to install [blender](https://www.blender.org/), because the program uses it to make the difference boolean. <br>
Then if you did not install it at the default location you must specify the blender path at launch or in config.py. <br>

## Use

### prerequisites

You must have :
- one or more 3D scan of mask in obj or stl format
- a software allowing to place points on a 3D object and to recover the coordinates of these said points. (**advise**)
- install this program

### preparing input data

The program needs input data to work. <br>
He needs one or more 3D scans in OBJ or STL format. <br>
If you have problem while detecting landmakrs, <br>
add for each scan having this problem a file containing the coordinates of the 51 landmarks in order in txt or pp format. <br>
Here is an overview of where to place these 51 landmarks and the order (precision is not very important): <br>
![Image showing the positions of the 51 landmarks](flameFitting/data/landmarks_51_annotated.png) <br>
(Image from [flame-fitting](https://github.com/Rubikplayer/flame-fitting)) <br>
Once all the requested files have been obtained, place them in the input folder.

### execution

Now that the input data is ready you can run the program, <br>
to do this, open a terminal / command prompt and run:
```
python main.py
```

### options

Several parameters are available here is the list (you can modify / see the default values ​​in config.py):
- ```--output_format```: output file format.
- ```--auto_lmk```: defines whether the 51 landmarks are generated automatically or not.
- ```--radius```: sphere radius used to generate mask holes when saving in stl or obj format
- ```--blender_path```: path of the folder containing [blender](https://www.blender.org/). (no need to change if installing in the default location offered by the installer [blender](https://www.blender.org/))

Here is an example of execution with parameter:
```
python main.py --output_format=stl --auto_lmk=True --blender_path="E:\\Program Files\\Blender Foundation\\Blender 3.2"
```

### retrieving output data

Once the execution is finished, you will find the output data in the output folder. <br>
For each scan you get a file containing the coordinates of the markers or the resulting hole mask. (depends on the chosen output format) <br>
The file has the same name as the input mask but with the extension corresponding to the output format.

### sizes

List of different supported formats:
- **npy**: numpy file that can be read with python thanks to numpy.
- **txt**: text file that can be read by Rhinoceros 3D or in a text editor or spreadsheet (equivalent to a .csv file).
- **pp**: picked points file that can be read by MeshLab, it is based on an HTML structure so you can open it with a text editor.
- **obj**: wavefront file (3D object), contains the hole starting mask from the marker points (**requires [blender](https://www.blender.org/)**)
- **stl**: stereolithography file (3D object) contains the hole starting mask from the marker points (**requires [blender](https://www.blender.org/)**)
  
## Resources

List of resources used (not exhaustive):
- [Flame](https://flame.is.tue.mpg.de/)
- [flame-fitting](https://github.com/Rubikplayer/flame-fitting)
- [eigen](https://gitlab.com/libeigen/eigen)
- [panda3d](https://www.panda3d.org/)
- [Visage-Generator](https://github.com/Carlier-Maxime/Visage-Generator)

## Version Packages

Version of packages used during development (You can also find its information in packages.txt in the doc folder):

[![chumpy : 0.70](https://img.shields.io/badge/chumpy-0.70-red)](https://github.com/mattloper/chumpy)
[![colorama : 0.4.5](https://img.shields.io/badge/colorama-0.4.5-brown)](https://github.com/tartley/colorama)
[![Cython : 0.29.21](https://img.shields.io/badge/Cython-0.29.21-orange)](https://github.com/cython/cython)
[![face--alignment : 1.3.5](https://img.shields.io/badge/face--alignment-1.3.5-bisque)](https://github.com/1adrianb/face-alignment)
[![imageio : 2.21.0](https://img.shields.io/badge/imageio-2.21.0-yellow)](https://github.com/imageio/imageio)
[![llvmlite : 0.39.0](https://img.shields.io/badge/llvmlite-0.39.0-gold)](https://github.com/numba/llvmlite)
[![networkx : 2.8.5](https://img.shields.io/badge/networkx-2.8.5-green)](https://github.com/networkx/networkx)
[![numba : 0.56.0](https://img.shields.io/badge/numba-0.56.0-olivedrab)](https://github.com/numba/numba)
[![numpy : 1.23.1](https://img.shields.io/badge/numpy-1.23.1-limegreen)](https://github.com/numpy/numpy)
[![opencv--python : 4.4.0.46](https://img.shields.io/badge/opencv--python-4.4.0.46-aquamarine)](https://github.com/opencv/opencv-python)
[![packaging : 21.3](https://img.shields.io/badge/packaging-21.3-steelblue)](https://github.com/pypa/packaging)
[![Panda3D : 1.10.11](https://img.shields.io/badge/Panda3D-1.10.11-teal)](https://github.com/panda3d/panda3d)
[![Pillow : 9.2.0](https://img.shields.io/badge/Pillow-9.2.0-skyblue)](https://github.com/python-pillow/Pillow)
[![psbody--mesh : 0.3](https://img.shields.io/badge/psbody--mesh-0.3-blue)](https://github.com/MPI-IS/mesh)
[![PyOpenGL : 3.1.6](https://img.shields.io/badge/PyOpenGL-3.1.6-blueviolet)](https://github.com/mcfletch/pyopengl)
[![pyparsing : 3.0.9](https://img.shields.io/badge/pyparsing-3.0.9-red)](https://github.com/pyparsing/pyparsing)
[![PyWavelets : 1.3.0](https://img.shields.io/badge/PyWavelets-1.3.0-brown)](https://github.com/PyWavelets/pywt)
[![PyYAML : 6.0](https://img.shields.io/badge/PyYAML-6.0-orange)](https://github.com/yaml/pyyaml)
[![pyzmq : 23.2.0](https://img.shields.io/badge/pyzmq-23.2.0-bisque)](https://github.com/zeromq/pyzmq)
[![scikit--image : 0.19.3](https://img.shields.io/badge/scikit--image-0.19.3-yellow)](https://github.com/scikit-image/scikit-image)
[![scipy : 1.9.0](https://img.shields.io/badge/scipy-1.9.0-gold)](https://github.com/scipy/scipy)
[![six : 1.16.0](https://img.shields.io/badge/six-1.16.0-green)](https://github.com/benjaminp/six)
[![tifffile : 2022.7.31](https://img.shields.io/badge/tifffile-2022.7.31-olivedrab)](https://github.com/cgohlke/tifffile)
[![torch : 1.12.0](https://img.shields.io/badge/torch-1.12.0-limegreen)](https://github.com/pytorch/pytorch)
[![tqdm : 4.64.0](https://img.shields.io/badge/tqdm-4.64.0-aquamarine)](https://github.com/tqdm/tqdm)
[![trimesh : 3.12.9](https://img.shields.io/badge/trimesh-3.12.9-steelblue)](https://github.com/mikedh/trimesh)
[![typing_extensions : 4.3.0](https://img.shields.io/badge/typing_extensions-4.3.0-teal)](https://github.com/python/typing_extensions)
[![Werkzeug : 1.0.1](https://img.shields.io/badge/Werkzeug-1.0.1-skyblue)](https://github.com/pallets/werkzeug)
[![zmq : 0.0.0](https://img.shields.io/badge/zmq-0.0.0-blue)](https://github.com/zeromq/pyzmq)
