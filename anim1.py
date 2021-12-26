import numpy as np
import math
from renderer.rendererFactory import createRenderer


points = np.loadtxt("raw.txt", delimiter=",")
renderer = createRenderer({'axisLabelEnable': True, 'axisScale': 1 / 2, 'axisFontSize': 300})


zMin = points.min(axis=0)[2]
zMax = points.max(axis=0)[2]

step = (zMax - zMin) / 10
bandWith = (zMax - zMin) / 5
start = zMin - bandWith
stop = zMin
color = [0.8, 0.1, 0.2]


angleStep = 10
angleBandWith = 45
angleStart = 0
angleStop = angleBandWith
angleColor = [0.1, 0.8, 0.2]

class ColorBuilder(object):

    def __init__(self, points):
        self.colors = np.zeros((len(points), 3))
        self.points = points

    def inZRange(self, color, start, stop):
        for i in range(0, len(self.points)):
            z = self.points[i][2]
            if z >= start and z <= stop:
                self.colors[i] = color
        return self

    def inAngleRange(self, color, diff, start, stop):
        for i in range(0, len(self.points)):
            angle = math.degrees(math.atan2(self.points[i][1], self.points[i][0] - diff))
            if angle < 0:
                angle += 360
            # if angle < 30 and angle > 0:
            # self.colors[i] = [self.colors[i][0] + color[0], self.colors[i][1] + color[1], self.colors[i][2] + color[2]]
            if angle >= start and angle <= stop:
                self.colors[i] = [self.colors[i][0] + color[0], self.colors[i][1] + color[1], self.colors[i][2] + color[2]]
        return self

    def build(self):
        return self.colors


while True:

    b = ColorBuilder(points)
    b.inZRange(color, start, stop)
    b.inAngleRange(angleColor, 0, angleStart, angleStop)

    renderer.render(points, b.build())
    start += step
    stop += step

    if start > zMax:
        start = zMin - bandWith
        stop = zMin

    angleStart += angleStep
    angleStop += angleStep

    if angleStop > 360:
        angleStart = 0
        angleStop = angleBandWith

    # time.sleep(0.05)


# v.show()
# painter = Painter(O3dRenderer())
# painter.show()
# v.show()
