import numpy as np
import time
import math
from rendererFactory import createRenderer
from lights import Lights

points = np.loadtxt("data/cone_test/cone_test_points_rand_15.csv", delimiter=",")


renderer = createRenderer()


def colorInRange(points, color, start, stop):
    colors = np.zeros((len(points), 3))
    for i in range(0, len(points)):
        z = points[i][2]
        if z >= start and z <= stop:
            colors[i] = color
        else:
            colors[i] = [0, 0.1, 0.5]

    return colors


step = 0.03
bandWith = 0.2
start = -bandWith
stop = 0
color = [0.8, 0.1, 0.2]

angleStep = 10
angleBandWith = 45
angleStart = 0
angleStop = angleBandWith
angleColor = [0.1, 0.8, 0.2]

class ColorBuilder(object):

    def __init__(self, lights):
        self.lights = lights

    def all(self, color):
        for i in range(0, len(self.lights)):
            bulb = self.lights[i].setColor(color)

        return self

    def inZRange(self, color, start, stop):
        for i in range(0, len(self.lights)):
            bulb = self.lights[i]
            z = self.lights[i].center[2]
            if z >= start and z <= stop:
                bulb.setColor(color)

        return self

    def inAngleRange(self, color, start, stop):
        for i in range(0, len(self.lights)):
            bulb = self.lights[i]
            x = bulb.center[0]
            y = bulb.center[1]
            angle = math.degrees(math.atan2(y, x))
            if angle < 0:
                angle += 360
            # if angle < 30 and angle > 0:
            # self.colors[i] = [self.colors[i][0] + color[0], self.colors[i][1] + color[1], self.colors[i][2] + color[2]]
            if angle >= start and angle <= stop:
                c = bulb.color
                bulb.setColor([color[0], color[1], color[2]])

        return self


lights = Lights.createLights(0.01, points)

while True:
    b = ColorBuilder(lights)
    b.all([0, 0, 0])
    b.inZRange(color, start, stop)
    b.inAngleRange(angleColor, angleStart, angleStop)

    renderer.render(lights.getPoints(), lights.getColors())
    start += step
    stop += step

    if start > 1.5:
        start = -bandWith
        stop = 0

    angleStart += angleStep
    angleStop += angleStep

    if angleStop > 360:
        angleStart = 0
        angleStop = angleBandWith

    time.sleep(0.05)


# v.show()
# painter = Painter(O3dRenderer())
# painter.show()
# v.show()
