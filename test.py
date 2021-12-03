import numpy as np
import time
import math
from painter import Painter
from renderer.o3dRenderer import O3dRenderer
from renderer.visualizer import visualizerOf

# painter = Painter(O3dRenderer())
# painter.show()
# v.show()


def moveXBy(points, xDiff):
    for i, p in enumerate(points):
        points[i] = [p[0] + xDiff, p[1], p[2]]


points_10 = np.loadtxt("data/cone_test/cone_test_points_rand_10.csv", delimiter=",")
points_15 = np.loadtxt("data/cone_test/cone_test_points_rand_15.csv", delimiter=",")
points_20 = np.loadtxt("data/cone_test/cone_test_points_rand_20.csv", delimiter=",")
points_30 = np.loadtxt("data/cone_test/cone_test_points_rand_30.csv", delimiter=",")
points_40 = np.loadtxt("data/cone_test/cone_test_points_rand_40.csv", delimiter=",")
points_50 = np.loadtxt("data/cone_test/cone_test_points_rand_50.csv", delimiter=",")
points_no = np.loadtxt("data/cone_test/cone_test_points_2.csv", delimiter=",")

moveXBy(points_10, 0)
moveXBy(points_15, 1.5)
moveXBy(points_20, 3)
moveXBy(points_30, 4.5)
moveXBy(points_40, 6)
moveXBy(points_50, 7.5)
# moveXBy(points_no, 9)
moveXBy(points_no, 3)

v = visualizerOf([], axis=True)
renderer_10 = O3dRenderer(v)
renderer_15 = O3dRenderer(v)
renderer_20 = O3dRenderer(v)
renderer_30 = O3dRenderer(v)
renderer_40 = O3dRenderer(v)
renderer_50 = O3dRenderer(v)
renderer_no = O3dRenderer(v)


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

    # renderer_10.render(points_10, ColorBuilder(points_10).inZRange(color, start, stop).inAngleRange(angleColor, 0, angleStart, angleStop).build())
    renderer_15.render(points_15, ColorBuilder(points_15).inZRange(color, start, stop).inAngleRange(angleColor, 1.5, angleStart, angleStop).build())
    # renderer_20.render(points_20, colorInRange(points_20, color, start, stop))
    # renderer_30.render(points_30, colorInRange(points_30, color, start, stop))
    # renderer_40.render(points_40, colorInRange(points_40, color, start, stop))
    # renderer_50.render(points_50, colorInRange(points_50, color, start, stop))
    renderer_no.render(points_no, ColorBuilder(points_no).inZRange(color, start, stop).inAngleRange(angleColor, 3, angleStart, angleStop).build())
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
