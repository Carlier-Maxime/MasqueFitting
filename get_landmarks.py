import sys
import os

from direct.showbase.ShowBase import ShowBase
from panda3d.core import DirectionalLight


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
        taskMgr.doMethodLater(1, self.screenshotTask, 'screenshot')

    def screenshotTask(self, task):
        if not os.path.isdir("tmp"):
            os.mkdir("tmp")
        base.screenshot("tmp/screen.png", False)
        return task.done


if __name__ == '__main__':
    args = sys.argv[1:]
    app = MyApp(str(args[0]))
    app.run()
