import os
import sys

import cv2
import numpy as np
from direct.showbase.ShowBase import ShowBase
from panda3d.core import DirectionalLight, ConfigVariableString, CollisionTraverser, \
    CollisionHandlerQueue, CollisionNode, CollisionRay, GeomNode

import util


class MyApp(ShowBase):

    def __init__(self, file_path):
        ShowBase.__init__(self)
        self.file_path = file_path
        model = self.loader.load_model(file_path)
        model.reparentTo(render)
        dlight = DirectionalLight('my dlight')
        dlnp = render.attachNewNode(dlight)
        dlnp.setPosHpr(0, 0, 500, 0, -84, 0)
        model.setLight(dlnp)
        base.disableMouse()
        base.setBackgroundColor(1, 1, 1)
        base.camera.setPosHpr(0, 0, 450, 0, -84, 0)

        # CollisionTraverser  and a Collision Handler is set up
        self.picker = CollisionTraverser()
        self.picker.showCollisions(render)
        self.pq = CollisionHandlerQueue()

        self.pickerNode = CollisionNode('mouseRay')
        self.pickerNP = camera.attachNewNode(self.pickerNode)
        self.pickerNode.setFromCollideMask(GeomNode.getDefaultCollideMask())
        self.pickerRay = CollisionRay()
        self.pickerNode.addSolid(self.pickerRay)
        self.picker.addCollider(self.pickerNP, self.pq)

        taskMgr.doMethodLater(0, self.screenshotTask, 'screenshot')

    def screenshotTask(self, task):
        print("screenshot")
        if not os.path.isdir("tmp"):
            os.mkdir("tmp")
        base.screenshot("tmp/screen.png", False)
        lmk = self.get_landmark_2d()
        util.save_points(lmk, self.file_path.split('.obj')[0], "pp")
        self.finalizeExit()
        return task.done

    def pixel_to_3d_point(self, x, y):
        # set the position of the ray based on the mouse position
        halfX = base.win.getXSize() / 2
        halfY = base.win.getYSize() / 2
        x = (x - halfX) / halfX
        y = ((y - halfY) / halfY)*-1
        self.pickerRay.setFromLens(base.camNode, x, y)
        self.picker.traverse(render)
        # if we have hit something sort the hits so that the closest is first and highlight the node
        if self.pq.getNumEntries() > 0:
            self.pq.sortEntries()
            entry = self.pq.getEntry(0)
            if entry.hasSurfacePoint():
                return entry.getSurfacePoint(entry.into_node_path)
        return None

    def read2d_landmark(self):
        img = cv2.imread("tmp/result.png")
        rows, cols = img.shape[:2]
        pts = []
        indcount = []
        for i in range(rows):
            for j in range(200, cols-250):
                p = img[i, j]
                if p[2] == 255 and p[0] == 0 and p[1] == 0:  # red beacause opencv is BGR not RGB !
                    if [i, j] not in indcount:
                        p3d = self.pixel_to_3d_point(j, i + 1)
                        if p3d is not None:
                            pts.append(p3d)
                        else:
                            y = i
                            while p3d is None and y < rows:
                                p3d = self.pixel_to_3d_point(j, y + 1)
                                y += 1
                            if p3d is not None:
                                pts.append(p3d)
                        for ind in [[i, j], [i+1, j-1], [i+1, j+1], [i+2, j]]:
                            indcount.append(ind)
                        if len(pts) >= 51:
                            return pts
        return pts

    def get_landmark_2d(self):
        os.chdir("lmk-detection")
        os.system("python lmk_detection.py ../tmp/screen.png")
        os.chdir("..")
        preds = np.load("lmk-detection/lmk.npy")
        pts = []
        for pred in preds:
            p = self.pixel_to_3d_point(pred[0], pred[1])
            if p is not None:
                pts.append(p)
            else:
                x, y = pred
                pasX, pasY = 0, 0
                if 200 <= y <= 400 and 300 <= x <= 500:
                    pasY = 1
                elif x < 400:
                    pasX = 1
                else:
                    pasX = -1
                while p is None and 0 <= x <= 800 and 0 <= y <= 600:
                    p = self.pixel_to_3d_point(x, y)
                    x += pasX
                    y += pasY
                if p is not None:
                    pts.append(p)
                else:
                    print(f'None 3D point for pixel {x}, {y} !')
        return pts[17:]


if __name__ == '__main__':
    args = sys.argv[1:]
    ConfigVariableString("window-type").setValue("offscreen")
    ConfigVariableString("model-cache-dir").setValue("")
    app = MyApp(str(args[0]))
    app.run()
