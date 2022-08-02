import sys
import warnings
import face_alignment
import numpy as np
from skimage import io


def run(file_path):
    warnings.filterwarnings("ignore", "No faces were detected.")
    fa = face_alignment.FaceAlignment(face_alignment.LandmarksType._2D, flip_input=False, device="cpu")
    input = io.imread(file_path)
    preds = fa.get_landmarks(input)
    if preds is None:
        preds = [[]]
    np.save("lmk.npy", preds[0])


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("not file path for image")
        sys.exit(1)
    run(str(sys.argv[1]))
