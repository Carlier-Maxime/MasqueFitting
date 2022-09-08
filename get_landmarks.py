import logging as log
import os
import sys

import cv2
import numpy as np
from direct.gui.OnscreenText import OnscreenText
from direct.showbase.ShowBase import ShowBase
from panda3d.core import DirectionalLight, CollisionTraverser, \
    CollisionHandlerQueue, CollisionNode, CollisionRay, GeomNode, loadPrcFile, LVecBase2f
from lmkDetection import lmk_detection

import util


class MyApp(ShowBase):
    def __init__(self, file_path: str, camX, camY, camZ, camH, camP, camR, fovI, fovJ,
                 lightX, lightY, lightZ, lightH, lightP, lightR):
        """
        Args:
            file_path (str): path file for 3D object
        """
        ShowBase.__init__(self)
        print("Prepare the scene")
        self.file_path = file_path
        model = self.loader.load_model(file_path)
        model.reparentTo(render)
        self.dlight = DirectionalLight('my dlight')
        dlnp = render.attachNewNode(self.dlight)
        dlnp.setPosHpr(lightX, lightY, lightZ, lightH, lightP, lightR)
        model.setLight(dlnp)
        base.disableMouse()
        base.setBackgroundColor(1, 1, 1)
        base.camera.setPosHpr(camX, camY, camZ, camH, camP, camR)
        base.camLens.setFov(LVecBase2f(fovI, fovJ))

        # CollisionTraverser  and a Collision Handler is set up
        print("Init laser for return 3D")
        self.picker = CollisionTraverser()
        self.picker.showCollisions(render)
        self.pq = CollisionHandlerQueue()

        self.pickerNode = CollisionNode('mouseRay')
        self.pickerNP = camera.attachNewNode(self.pickerNode)
        self.pickerNode.setFromCollideMask(GeomNode.getDefaultCollideMask())
        self.pickerRay = CollisionRay()
        self.pickerNode.addSolid(self.pickerRay)
        self.picker.addCollider(self.pickerNP, self.pq)

        taskMgr.doMethodLater(0, self.MainTask, 'MainTask')
        #self.enable_mouve_camera()

    def enable_mouve_camera(self) -> None:
        """
        enable the movement of the camera by the keyboard and the possibility of see the position of the camera.
        Returns: None
        """
        self.accept('q', self.move, [0, 0.01, 0, 0, 0, 0, 0])
        self.accept('d', self.move, [0, -0.01, 0, 0, 0, 0, 0])
        self.accept('s', self.move, [0.01, 0, 0, 0, 0, 0, 0])
        self.accept('z', self.move, [-0.01, 0, 0, 0, 0, 0, 0])
        self.accept('a', self.move, [0, 0, 0.01, 0, 0, 0, 0])
        self.accept('e', self.move, [0, 0, -0.01, 0, 0, 0, 0])
        self.accept('y', self.move, [0, 0, 0, 1, 0, 0, 0])
        self.accept('h', self.move, [0, 0, 0, -1, 0, 0, 0])
        self.accept('p', self.move, [0, 0, 0, 0, 1, 0, 0])
        self.accept('m', self.move, [0, 0, 0, 0, -1, 0, 0])
        self.accept('r', self.move, [0, 0, 0, 0, 0, 1, 0])
        self.accept('f', self.move, [0, 0, 0, 0, 0, -1, 0])
        self.accept('i', self.move, [0, 0, 0, 0, 0, 0, -1])
        self.accept('o', self.move, [0, 0, 0, 0, 0, 0, 1])
        self.accept('c', self.ShowCamPos)
        self.accept('c-up', self.HideCamPos)

    def move(self, x: float, y: float, z: float, h: float, p: float, r: float, fov: int) -> None:
        """
        change the position, rotation and field of view of the camera by adding the values provided
        Args:
            x (float): value to add a position in the X axis
            y (float): value to add a position in the Y axis
            z (float): value to add a position in the Z axis
            h (float): value to add a rotation in the heading
            p (float): value to add a rotation in the pitch
            r (float): value to add a rotation in the row
            fov (int): value to add a field of view

        Returns: None
        """
        base.camera.setX(base.camera.getX() + x)
        base.camera.setY(base.camera.getY() + y)
        base.camera.setZ(base.camera.getZ() + z)
        base.camera.setH(base.camera.getH() + h)
        base.camera.setP(base.camera.getP() + p)
        base.camera.setR(base.camera.getR() + r)
        base.camLens.setFov(base.camLens.getFov() + fov)

    def ShowCamPos(self) -> None:
        """
        Display Information of the position of the camera (position, rotation, field of view)
        Returns: None
        """
        x = base.camera.getX()
        y = base.camera.getY()
        z = base.camera.getZ()
        h = base.camera.getH()
        p = base.camera.getP()
        r = base.camera.getR()
        fov = base.camLens.getFov()
        self.title = OnscreenText(
            text=str(x) + " : " + str(y) + " : " + str(z) + "\n" + str(h) + " : " + str(p) + " : " + str(
                r) + " : " + str(fov),
            style=1, fg=(1, 1, 0, 1), pos=(0, 0), scale=0.07)

    def HideCamPos(self) -> None:
        """
        turn off camera information
        Returns: None
        """
        self.title.destroy()

    def MainTask(self, task):
        """
        screenshot scene,
        detect 3D landmark,
        save landmark.
        Args:
            task: task object
        """
        print("Screenshot scene view")
        if not os.path.isdir("tmp"):
            os.mkdir("tmp")
        base.screenshot("tmp/screen.png", False)

        print("Detect the 3D landmarks..")
        lmk = self.get_landmark_3d()
        if lmk is None:
            if self.dlight.color != (0.2, 0.2, 0.2, 1.0):
                self.dlight.color = (0.2, 0.2, 0.2, 1.0)
                log.info("landmarks not found, change light intensity and retry")
                taskMgr.doMethodLater(0, self.MainTask, 'MainTask')
            else:
                log.error("the landmarks are be not found")
                exit(1)
            return task.done
        print("Save landmarks")
        util.save_points(lmk, self.file_path.split('.obj')[0], "pp")
        sys.tracebacklimit = 0
        raise KeyboardInterrupt("for stop panda3d not all prgm")
        return task.done

    def pixel_to_3d_point(self, x, y):
        """
        Transform pixel coordinate on the window into the 3D point
        Args:
            x (int): position X in the window
            y (int): position Y in the window
        Returns: 3D Point
        """
        # set the position of the ray based on the mouse position
        halfX = base.win.getXSize() / 2
        halfY = base.win.getYSize() / 2
        x = (x - halfX) / halfX
        y = ((y - halfY) / halfY) * -1
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
        """
        Read the 3D landmarks in the picture
        Returns: 2D landmarks
        """
        img = cv2.imread("tmp/result.png")
        rows, cols = img.shape[:2]
        pts = []
        indcount = []
        for i in range(rows):
            for j in range(200, cols - 250):
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
                        for ind in [[i, j], [i + 1, j - 1], [i + 1, j + 1], [i + 2, j]]:
                            indcount.append(ind)
                        if len(pts) >= 51:
                            return pts
        return pts

    def get_landmark_3d(self):
        """
        Obtain the 3D landmarks, the method used :
        detect 2D landmark, transform 2D to 3D.
        Returns: 3D landmarks
        """
        print("Detect 2D landmarks")
        os.chdir("lmkDetection")
        lmk_detection.run("../tmp/screen.png")
        os.chdir("..")
        preds = np.load("lmkDetection/lmk.npy")
        if len(preds) == 0:
            return None
        pts = []
        print("Transform 2D landmarks to 3D landmarks")
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
                    log.error(f'No 3D point fot the pixel {x}, {y} !')
        return pts[17:]

    def finalizeExit(self):
        return


def run(file_path, camX=0, camY=0, camZ=450, camH=0, camP=-84, camR=0, fovI=39.3201, fovJ=30, lightX=0,
        lightY=0, lightZ=500, lightH=0, lightP=-84, lightR=0):
    print("Configuration of panda3d")
    loadPrcFile("etc/Config.prc")
    app = MyApp(file_path, camX, camY, camZ, camH, camP, camR, fovI, fovJ, lightX, lightY, lightZ, lightH, lightP, lightR)
    app.run()
    sys.tracebacklimit = 1000


if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args) < 1:
        print("Missing arguments")
        exit(1)
    run(str(args[0]))
