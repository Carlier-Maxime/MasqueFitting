# Masque Fitting

## Description

Masque Fitting vous permet à partir d'un scan 3D et des coordonnées des 51 landmark (voir [Utilisation](#utilisation)), <br>
d'obtenir les coordonnées des N marqueur correspondant aux points choisie <br>
sur le visage flame. Par défaut ils vous retournent ces 105 points :
![Représentation des 105 points](105points.gif) <br>
(Cette image est un gif d'illustration issue de [VisageGenerator](https://github.com/Carlier-Maxime/Visage-Generator)) <br>
Bien entendu les coordonnées de ces 105 points sont adapté afin de collé aux masque fournie.


## Installation

### Pré-requis

Pour installer / éxécuter Masque Fitting vous devez avoir :
- [python](https://www.python.org/) (pour éxécutez les fichier python dont ce programme)
- [git](https://git-scm.com/) (pour récupérer les dépendance présant sur des dépot git ([psbody-mesh](https://github.com/MPI-IS/mesh) et [eigen](https://gitlab.com/libeigen/eigen)))
- **g++** (pas tester si nécessaire, mais je suppose qu'il est nécessaire pour compiler [eigen](https://gitlab.com/libeigen/eigen))
- **7zip** ou tout autre gestionnaire de fichier zip afin de dézipper le fichier model

### Model

Télécharger le model flame (celui de 2020 de préférence) [ici](https://flame.is.tue.mpg.de/)
et dézipper l'archive obtenue puis placer son contenu (les 3 fichier model) dans flame-fitting/models.

### Dépendance

Ouvrez un terminal ou un invite de commande et lancer le fichier d'installation :
```
python INSTALL.py
```

## Utilisation

### pré-requis

Vous devez avoir :
- un ou plusieur scan 3D de masque au format obj
- un logiciel permettant de placer des point sur un objet 3D et de récupérer les coordonnées de ces dit points.
- installer ce programme

### préparation des données d'entrée

Le programme a besoin pour fonctionner de données d'entrée. <br>
Il lui faut un ou plusieur scan 3D au format obj et avec pour chaque scan un fichier contenant les coordonnées des 51 landmark au format txt ou pp. <br>
Voici une aperçu de là où il faut placer ces 51 landmark :
![Image montrant les position des 51 landmark](./flame-fitting/data/landmarks_51_annotated.png)
Une fois tous les fichier demander obtenue placer les dans le dossier input.

### éxécution

Maintenant que les données d'entré sont prête vous pouvez éxécuter le programme, <br>
pour cela ouvrez un terminal / invite de commande et éxécuter :
```
python main.py
```

### récupération des données de sortie

Une fois l'éxécution terminer, vous retrouverer les données de sortie dans le dossier output.
Pour chaque scan il vous ressort un fichier contenant les coordonnées des marqueurs.
Le fichier à le même nom que le scan mais avec une extension différente.

### options

Vous pouvez paramètrez le type de format pour le fichier de sortie,
en le spécifiant lors du lancement du programme. <br>
Voici un exemple pour le format txt :
```
python main.py --output_format=txt
```

Si vous n'aimez pas spécifier à chaque lancement du programme le format de sortie, <br>
rendez-vous dans le fichier **config.py** et changer la valeur par défaut.

### formats

Liste des différent format prise en charge :
- **npy** : fichier numpy pouvant être lu avec python grâce à numpy.
- **txt** : fichier texte pouvant être lu par Rhinoceros 3D ou dans un éditeur de texte.
- **pp** : fichier picked points pouvant être lu par MeshLab, <br> 
  il se base sur une structure HTML vous pouvez donc l'ouvrir avec un éditeur de texte.
  
## Ressources

Liste des resources utilisée :
- [Flame](https://flame.is.tue.mpg.de/)
- [flame-fitting](https://github.com/Rubikplayer/flame-fitting)
- [eigen](https://gitlab.com/libeigen/eigen)
- [Visage-Generator](https://github.com/Carlier-Maxime/Visage-Generator)