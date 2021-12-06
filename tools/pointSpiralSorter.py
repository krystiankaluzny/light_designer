import numpy as np
import time
import math
import sys
import random
import matplotlib.pyplot as plt
from dataclasses import dataclass


sys.path.append('../')

from renderer.o3dRenderer import O3dRenderer
from renderer.visualizer import visualizerOf, visualizerWithEditingOf
from tools.pointCloudData import PointCloudData, NotBrownColorFilter


class ColorBuilder(object):

    def __init__(self, points):
        self.colors = np.zeros((len(points), 3))
        self.points = points

    def inIndexRange(self, color, start, stop):
        for i in range(0, len(self.points)):
            if i >= start and i <= stop:
                self.colors[i] = color
        return self

    def build(self):
        return self.colors


@dataclass
class PointSlice(object):
    id: int
    points: list

    def add(self, point):
        self.points.append(point)

    def pointAngle(self, point):
        angle = math.degrees(math.atan2(point[1], point[0]))
        if angle < 0:
            angle += 360
        return angle

    def sort(self):
        self.points.sort(key=self.pointAngle)

    def getColor(self):
        return np.asarray(plt.get_cmap("tab20")(self.id))[:3]

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
        r = 0.1
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

    def getPoints(self, count):
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

    def getColors(self, count):
        npColors = np.zeros((0, 3))
        for i in range(min(len(self.bulbs), count)):
            bulb = self.bulbs[i]
            npColors = np.append(npColors, bulb.bulbColors, axis=0)

        return npColors


points = np.loadtxt("../data/lights/lights_4_upright_manual_selected.csv", delimiter=",")


zMin = points.min(axis=0)[2]
zMax = points.max(axis=0)[2]

sliceCount = 20
sliceWith = zMax / sliceCount
print(sliceWith)

pointSlices = dict()

for i in range(0, len(points)):
    p = points[i]
    z = p[2]
    sliceId = int(z / sliceWith)
    # print(z, sliceId)
    if sliceId in pointSlices:
        pointSlice = pointSlices[sliceId]
    else:
        pointSlice = PointSlice(sliceId, [])
        pointSlices[sliceId] = pointSlice

    pointSlice.add(p)

print(zMin, zMax)
print(len(pointSlices))


npPoints = np.zeros((0, 3))
npColors = np.zeros((0, 3))


for sliceId in range(0, sliceCount + 1):
    if sliceId in pointSlices:
        pointSlice = pointSlices[sliceId]
        pointSlice.sort()
        for i in range(0, len(pointSlice.points)):
            npPoints = np.append(npPoints, [pointSlice.points[i]], axis=0)
            npColors = np.append(npColors, [pointSlice.getColor()], axis=0)

lights = Lights()
for i in range(0, len(points)):
    lights.add(points[i], [1, 0, 0])


# np.savetxt("../data/lights/lights_4_upright_presorted.csv", npPoints, delimiter=",")

inputFile = "../data/point_clouds/decerto_choinka_4_upright.ply"
pointCloudData = PointCloudData.initFromFile(inputFile)
colorFiltered = NotBrownColorFilter().filter(pointCloudData)

# v = visualizerOf([], axis=True)
v = visualizerWithEditingOf([], axis=False)
renderer = O3dRenderer(v)
v.addGeometry([colorFiltered.toPointCloud()])

count = 1
v.show()

p = v.vis.get_picked_points()
print(p)

for index in p:
    x = colorFiltered.npPoints[index][0]
    y = colorFiltered.npPoints[index][1]
    z = colorFiltered.npPoints[index][2]
    print(f"{x},{y},{z}")


def incrementCount(vis):
    global count
    count += 1
    print("count", count)
    return False


def decrementCount(vis):
    global count
    count -= 1
    print("count", count)
    return False


# v.vis.register_key_callback(ord("I"), incrementCount)
# v.vis.register_key_callback(ord("O"), decrementCount)


while True:
    # count = int(input("Liczba lampek do zapalenia: "))
    renderer.render(lights.getPoints(count), lights.getColors(count))

    time.sleep(0.05)
