# Masque Fitting

## Description

Masque Fitting vous permet à partir d'un scan 3D d'obtenir les coordonnées des N marqueur correspondant aux points choisie sur le visage flame. (voir [Utilisation](#utilisation)) <br>
Par défaut ils vous retournent ces 105 points : <br>
![Représentation des 105 points](doc/105points.gif) <br>
(Cette image est un gif d'illustration issue de [VisageGenerator](https://github.com/Carlier-Maxime/Visage-Generator)) <br>
Bien entendu les coordonnées de ces 105 points sont adapté afin de collé aux masque fournie.


## Installation

### Pré-requis

Pour installer / éxécuter Masque Fitting vous devez avoir :
- [python](https://www.python.org/) (pour éxécutez les fichier python dont ce programme)
- [git](https://git-scm.com/) (pour récupérer les dépendance présant sur des dépot git ([psbody-mesh](https://github.com/MPI-IS/mesh) et [eigen](https://gitlab.com/libeigen/eigen)))
- **g++** (pas tester si nécessaire, mais je suppose qu'il est nécessaire pour compiler [eigen](https://gitlab.com/libeigen/eigen))
- [7zip](https://www.7-zip.org/download.html) ou tout autre gestionnaire de fichier zip afin de dézipper le fichier model

### Récupération

Cloner simplement le projet à l'aide de git dans le répertoire de votre choix :
```
git clone https://github.com/Carlier-Maxime/MasqueFitting
```

### Dépendance

Ouvrez un terminal ou un invite de commande et lancer le fichier d'installation :
```
python INSTALL.py
```

Si vous voulez installer manuellement les dépendance, voici quelques information : <br>

- la liste des dépendance requise se trouve dans les fichier requirements.txt (sauf exception)
- pour psbody-mesh il faudra probalement installer [boost](https://www.boost.org/)
- Pour installer psbody-mesh sous Windows prener la version présent sur ce [dépôt](https://github.com/johnbanq/mesh/tree/fix/MSVC_compilation)
- la plupart des dépendance s'installe avec ```pip install <name_package>``` ou éxécuter ```pip install -r requirements.txt``` qui installera tous les packages requis. sur Windows éxécuter plutôt ```pip install -r requirements_windows.txt```
- lmk-detection utilse numba qui demande une version de numpy antèrieur, Or pour l'utilisation faite il fonctionne avec une version supérieur. <br>
Du coup aller dans le dossier numba (venv/Lib/site-packages/numba sur Windows si installer dans un virtualenv python), dans le fichier \_\_init\_\_.py et supprimer les 2 ligne indiquant la version minimal de numpy (L145-L146).
- par défaut vous devez installer eigen dans flame-fitting/sbody/alignment/mesh-distance. <br>
Pour plus d'information liser le readme de flame-fitting
- pour installer eigen sous windows au lieu de éxécuter ```make``` éxécuter ```python setup.py build_ext --inplace```

en éspérant que ces information pour l'installation manuelle vous auront était utile.
Vous pouvez aussi regarder directement dans le fichier INSTALL.py pour mieux voir les étapes.

### Model

Télécharger le model flame (celui de 2020 de préférence) [ici](https://flame.is.tue.mpg.de/)
et dézipper l'archive obtenue puis placer son contenu (les 3 fichier model) dans flame-fitting/models.
(Vous pouvez vous le faire en même tant que l'installation.)

### Addon

Vous pouvez utiliser les points directement pour les transformer en sphere et faire la difference boolean sur le masque d'entrée <br>
afin d'obtenir directement le masque d'entrée au lieu d'un nuages de points. (format d'enregistrement OBJ et STL supporté) <br>
pour cela il est nécessaire de installer [blender](https://www.blender.org/), car le programme l'utilise pour faire la difference boolean. <br>
Ensuite si vous ne l'avez pas installer à l'endroit par défaut vous devez spécifier le chemin blender au lancement ou dans config.py. <br>

## Utilisation

### pré-requis

Vous devez avoir :
- un ou plusieur scan 3D de masque au format obj ou stl
- un logiciel permettant de placer des point sur un objet 3D et de récupérer les coordonnées de ces dit points. (**conseiller**)
- installer ce programme

### préparation des données d'entrée

Le programme a besoin pour fonctionner de données d'entrée. <br>
Il lui faut un ou plusieur scan 3D au format OBJ ou STL. <br>
Si vous avez un problème lors de la détection de landmakrs, <br>
ajouter pour chaque scan ayant ce problème un fichier contenant les coordonnées des 51 landmark dans l'ordre au format txt ou pp. <br>
Voici une aperçu de là où il faut placer ces 51 landmark et de l'ordre (la précision n'est pas très importante) : <br>
![Image montrant les position des 51 landmark](flameFitting/data/landmarks_51_annotated.png) <br>
(Image issue de [flame-fitting](https://github.com/Rubikplayer/flame-fitting)) <br>
Une fois tous les fichier demander obtenue placer les dans le dossier input.

### éxécution

Maintenant que les données d'entré sont prête vous pouvez éxécuter le programme, <br>
pour cela ouvrez un terminal / invite de commande et éxécuter :
```
python main.py
```

### options

Plusieur paramètre sont disponnible en voici la liste (vous pouvez modifier / voir les valeur par défaut dans config.py) :
- ```--output_format``` : format du fichier de sortie.
- ```--auto_lmk``` : définie si les 51 landmarks sont générés de manière automatique ou non.
- ```--radius``` : rayon des spheres utilisée pour généré les trou des masque lors de l'enregistrement dans le format stl ou obj
- ```--blender_path``` : chemin du dossier contenant [blender](https://www.blender.org/). (inutile de changer si installer à l'endroit par défaut proposer par l'installateur [blender](https://www.blender.org/))

Voici un exemple d'éxécution avec paramètre :
```
python main.py --output_format=stl --auto_lmk=True --blender_path="E:\\Program Files\\Blender Foundation\\Blender 3.2"
```

### récupération des données de sortie

Une fois l'éxécution terminer, vous retrouverer les données de sortie dans le dossier output. <br>
Pour chaque scan il vous ressort un fichier contenant les coordonnées des marqueurs ou le masque trouer resultant. (dépand du format de sortie choisie) <br>
Le fichier à le même nom que le masque d'entrée mais avec l'extension correspondant au format de sortie.

### formats

Liste des différent format prise en charge :
- **npy** : fichier numpy pouvant être lu avec python grâce à numpy.
- **txt** : fichier texte pouvant être lu par Rhinoceros 3D ou dans un éditeur de texte ou un tableur (équivaut à un fichier .csv).
- **pp** : fichier picked points pouvant être lu par MeshLab, il se base sur une structure HTML vous pouvez donc l'ouvrir avec un éditeur de texte.
- **obj** : fichier wavefront (objet 3D),  contient le masque de départ trouer à partir des points des marker (**nécessite [blender](https://www.blender.org/)**)
- **stl** : fichier stéréolithographie (objet 3D) contient le masque de départ trouer à partir des points des marker (**nécessite [blender](https://www.blender.org/)**)
  
## Ressources

Liste des resources utilisée (non exaustive) :
- [Flame](https://flame.is.tue.mpg.de/)
- [flame-fitting](https://github.com/Rubikplayer/flame-fitting)
- [eigen](https://gitlab.com/libeigen/eigen)
- [panda3d](https://www.panda3d.org/)
- [Visage-Generator](https://github.com/Carlier-Maxime/Visage-Generator)

## Version Packages

Version des packages utilisée lors du développement (Vous pouvez aussi retrouver ses informations dans packages.txt dans le dossier doc) :

![chumpy : 0.70](https://img.shields.io/badge/chumpy-0.70-red)
![colorama : 0.4.5](https://img.shields.io/badge/colorama-0.4.5-brown)
![Cython : 0.29.21](https://img.shields.io/badge/Cython-0.29.21-orange)
![face--alignment : 1.3.5](https://img.shields.io/badge/face--alignment-1.3.5-bisque)
![imageio : 2.21.0](https://img.shields.io/badge/imageio-2.21.0-yellow)
![llvmlite : 0.39.0](https://img.shields.io/badge/llvmlite-0.39.0-gold)
![networkx : 2.8.5](https://img.shields.io/badge/networkx-2.8.5-green)
![numba : 0.56.0](https://img.shields.io/badge/numba-0.56.0-olivedrab)
![numpy : 1.23.1](https://img.shields.io/badge/numpy-1.23.1-limegreen)
![opencv--python : 4.4.0.46](https://img.shields.io/badge/opencv--python-4.4.0.46-aquamarine)
![packaging : 21.3](https://img.shields.io/badge/packaging-21.3-steelblue)
![Panda3D : 1.10.11](https://img.shields.io/badge/Panda3D-1.10.11-teal)
![Pillow : 9.2.0](https://img.shields.io/badge/Pillow-9.2.0-skyblue)
![psbody--mesh : 0.3](https://img.shields.io/badge/psbody--mesh-0.3-blue)
![PyOpenGL : 3.1.6](https://img.shields.io/badge/PyOpenGL-3.1.6-blueviolet)
![pyparsing : 3.0.9](https://img.shields.io/badge/pyparsing-3.0.9-red)
![PyWavelets : 1.3.0](https://img.shields.io/badge/PyWavelets-1.3.0-brown)
![PyYAML : 6.0](https://img.shields.io/badge/PyYAML-6.0-orange)
![pyzmq : 23.2.0](https://img.shields.io/badge/pyzmq-23.2.0-bisque)
![scikit--image : 0.19.3](https://img.shields.io/badge/scikit--image-0.19.3-yellow)
![scipy : 1.9.0](https://img.shields.io/badge/scipy-1.9.0-gold)
![six : 1.16.0](https://img.shields.io/badge/six-1.16.0-green)
![tifffile : 2022.7.31](https://img.shields.io/badge/tifffile-2022.7.31-olivedrab)
![torch : 1.12.0](https://img.shields.io/badge/torch-1.12.0-limegreen)
![tqdm : 4.64.0](https://img.shields.io/badge/tqdm-4.64.0-aquamarine)
![trimesh : 3.12.9](https://img.shields.io/badge/trimesh-3.12.9-steelblue)
![typing_extensions : 4.3.0](https://img.shields.io/badge/typing_extensions-4.3.0-teal)
![Werkzeug : 1.0.1](https://img.shields.io/badge/Werkzeug-1.0.1-skyblue)
![zmq : 0.0.0](https://img.shields.io/badge/zmq-0.0.0-blue)
