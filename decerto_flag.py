import numpy as np
import time
import math
import random
from PIL import Image
from rendererFactory import createRenderer


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


zMin = points.min(axis=0)[2]
zMax = points.max(axis=0)[2]
zH = 3 * zMax / 4


print("zMin", zMin, "zMax", zMax)

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


img = Image.open('data/images/decerto_flag.jpg')
ary = np.array(img)
width = len(ary)
height = len(ary[0])


def zToJ(z):
    return int(z / zH * height)


def xyToI(x, y):
    angle = math.degrees(math.atan2(y, x))
    if angle < 0:
        angle += 360

    return int(angle / 180 * width)


npPoints = np.zeros((0, 3))
npColors = np.zeros((0, 3))

for i in range(len(ary)):
    for j in range(len(ary[i])):
        npPoints = np.append(npPoints, [[i, j, 0]], axis=0)
        npColors = np.append(npColors, [[ary[i][j][0] / 256, ary[i][j][1] / 255, ary[i][j][2] / 256]], axis=0)

class LighBulb(object):

    def __init__(self, index, center, color):
        self.index = index
        self.center = center
        self.color = color
        self.bulbPoints = self.generateBulb(center)
        self.bulbColors = np.zeros((len(self.bulbPoints), 3))
        self.setColor(color)

    def generateBulb(self, center):
        npPoints = np.zeros((0, 3))
        npPoints = np.append(npPoints, [center], axis=0)
        i = 0
        while i < 100:
            p = self.randPoint(center)
            if p is not None:
                npPoints = np.append(npPoints, [p], axis=0)
                i += 1

        return npPoints

    def randPoint(self, center):
        r = 0.01
        dx = random.uniform(-r, +r)
        dy = random.uniform(-r, +r)
        dz = random.uniform(-r, +r)
        if pow(dx, 2) + pow(dy, 2) + pow(dz, 2) <= pow(r, 2):
            return [center[0] + dx, center[1] + dy, center[2] + dz]

        return None

    def setColor(self, color):
        for i in range(len(self.bulbColors)):
            self.bulbColors[i] = color


class Lights(object):

    def __init__(self):
        self.lastIndex = -1
        self.bulbs = list()

    def add(self, center, color):
        self.lastIndex += 1
        self.bulbs.append(LighBulb(self.lastIndex, center, color))

    def getPoints(self):
        npPoints = np.zeros((0, 3))
        for bulb in self.bulbs:
            npPoints = np.append(npPoints, bulb.bulbPoints, axis=0)

        return npPoints

    def getPointsCount(self, count):
        npPoints = np.zeros((0, 3))
        for i in range(min(len(self.bulbs), count)):
            bulb = self.bulbs[i]
            npPoints = np.append(npPoints, bulb.bulbPoints, axis=0)

        return npPoints

    def getColors(self):
        npColors = np.zeros((0, 3))
        for bulb in self.bulbs:
            npColors = np.append(npColors, bulb.bulbColors, axis=0)

        return npColors

    def getColorsCount(self, count):
        npColors = np.zeros((0, 3))
        for i in range(min(len(self.bulbs), count)):
            bulb = self.bulbs[i]
            npColors = np.append(npColors, bulb.bulbColors, axis=0)

        return npColors


lights = Lights()
# colors = np.zeros((len(points), 3))

for index in range(len(points)):
    p = points[index]
    i = xyToI(p[0], p[1])
    j = zToJ(p[2])

    # lights.add(p, [1, 0, 0])
    if i >= 0 and j >= 0 and i < width and j < height:
        lights.add(p, [ary[i][j][0] / 256, ary[i][j][1] / 255, ary[i][j][2] / 256])
        # colors[index] = [ary[i][j][0] / 256, ary[i][j][1] / 255, ary[i][j][2] / 256]


while True:
    # renderer.render(npPoints, npColors)
    renderer.render(lights.getPoints(), lights.getColors())
    time.sleep(0.05)
