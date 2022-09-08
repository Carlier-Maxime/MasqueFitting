import argparse

parser = argparse.ArgumentParser(description='Masque Fitting')

parser.add_argument(
    '--output_format',
    type=str,
    default="npy",
    help="Le format de fichier dans lequel les coordonnées des marqueurs sort."
)

parser.add_argument(
    '--auto_lmk',
    type=bool,
    default=False,
    help="Activer ou désactiver la génération automatique de landmark"
)

parser.add_argument(
    '--radius',
    type=float,
    default=1.0,
    help="rayon des sphere pour représenter les points dans le format obj"
)

parser.add_argument(
    '--blender_path',
    type=str,
    default="./blender",
    help="chemin d'accès vers le dossier de blender (utile si n'est pas installer au endroit par default)"
)

parser.add_argument(
    '--panda3d_camera_x',
    type=float,
    default=0,
    help="argument for camera panda3d"
)

parser.add_argument(
    '--panda3d_camera_y',
    type=float,
    default=0,
    help="argument for camera panda3d"
)

parser.add_argument(
    '--panda3d_camera_z',
    type=float,
    default=-450,
    help="argument for camera panda3d"
)

parser.add_argument(
    '--panda3d_camera_h',
    type=float,
    default=0,
    help="argument for camera panda3d"
)

parser.add_argument(
    '--panda3d_camera_p',
    type=float,
    default=-84,
    help="argument for camera panda3d"
)

parser.add_argument(
    '--panda3d_camera_r',
    type=float,
    default=0,
    help="argument for camera panda3d"
)

parser.add_argument(
    '--panda3d_fov_i',
    type=float,
    default=39.3201,
    help="argument for fov panda3d"
)

parser.add_argument(
    '--panda3d_fov_j',
    type=float,
    default=30,
    help="argument for fov panda3d"
)

parser.add_argument(
    '--panda3d_light_x',
    type=float,
    default=0,
    help="argument for light panda3d"
)

parser.add_argument(
    '--panda3d_light_y',
    type=float,
    default=0,
    help="argument for light panda3d"
)

parser.add_argument(
    '--panda3d_light_z',
    type=float,
    default=500,
    help="argument for light panda3d"
)

parser.add_argument(
    '--panda3d_light_h',
    type=float,
    default=0,
    help="argument for light panda3d"
)

parser.add_argument(
    '--panda3d_light_p',
    type=float,
    default=-84,
    help="argument for light panda3d"
)

parser.add_argument(
    '--panda3d_light_r',
    type=float,
    default=0,
    help="argument for light panda3d"
)

parser.add_argument(
    '--input_flame_visage',
    type=bool,
    default=False,
    help="use flame visage in input"
)


def get_config():
    config = parser.parse_args()
    return config
