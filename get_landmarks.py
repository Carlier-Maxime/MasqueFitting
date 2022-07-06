import sys
import os
from datetime import datetime

import cv2
import numpy as np

from direct.showbase.ShowBase import ShowBase
from panda3d.core import DirectionalLight, Texture, NodePath, Filename, ConfigVariableString, CollisionTraverser, \
    CollisionHandlerQueue, CollisionNode, CollisionRay, GeomNode


class MyApp(ShowBase):

    def __init__(self, file_path):
        ShowBase.__init__(self)
        model = self.loader.load_model(file_path)
        model.reparentTo(render)
        dlight = DirectionalLight('my dlight')
        dlnp = render.attachNewNode(dlight)
        dlnp.setPosHpr(0, 0, 300, 0, -84, 0)
        render.setLight(dlnp)
        base.disableMouse()
        base.setBackgroundColor(1, 1, 1)
        base.camera.setPosHpr(0, 0, 300, 0, -84, 0)

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
        lmk = self.read2d_landmark()
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
            for j in range(cols):
                p = img[i, j]
                if p[2] == 255 and p[0] == 0 and p[1] == 0:  # red beacause opencv is BGR not RGB !
                    if [i, j] not in indcount:
                        pts.append(self.pixel_to_3d_point(j, i+1))
                        for ind in [[i, j], [i+1, j-1], [i+1, j+1], [i+2, j]]:
                            indcount.append(ind)
                        if len(pts) >= 61:
                            return pts
        return pts


if __name__ == '__main__':
    args = sys.argv[1:]
    ConfigVariableString("window-type").setValue("offscreen")
    app = MyApp(str(args[0]))
    app.run()
