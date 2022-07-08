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


def get_config():
    config = parser.parse_args()
    return config
