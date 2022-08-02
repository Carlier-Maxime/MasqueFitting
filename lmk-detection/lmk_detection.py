import sys
import warnings
import face_alignment
import numpy as np
from skimage import io

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("not file path for image")
        sys.exit(1)
    warnings.filterwarnings("ignore", "No faces were detected.")
    fa = face_alignment.FaceAlignment(face_alignment.LandmarksType._2D, flip_input=False, device="cpu")
    input = io.imread(str(sys.argv[1]))
    preds = fa.get_landmarks(input)
    if preds is None:
        preds = [[]]
    np.save("lmk.npy", preds[0])
