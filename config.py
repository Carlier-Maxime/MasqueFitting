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
    '--python_version',
    type=str,
    default="",
    help="version de python utiliser si 3.9 "
         "utilise python3.9 lors de l'appel d'autre programme python au lieu d'utiliser python"
)

parser.add_argument(
    '--blender_path',
    type=str,
    default="./blender",
    help="chemin d'accès vers le dossier de blender (utile si n'est pas installer au endroit par default)"
)


def get_config():
    config = parser.parse_args()
    return config
