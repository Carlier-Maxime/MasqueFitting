import os


def run():
    if not os.path.exists('flame-fitting/models/generic_model.pkl'):
        print("Télécharger le  flame model ! (plus d'information dans README.md)")


if __name__ == '__main__':
    run()
