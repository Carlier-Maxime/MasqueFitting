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
    default=0.5,
    help="rayon des sphere pour représenter les points dans le format obj"
)


def get_config():
    config = parser.parse_args()
    return config
