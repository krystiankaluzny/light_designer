import numpy as np
import time
import math
import sys
import random
import matplotlib.pyplot as plt
import open3d as o3d
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
        r = 0.15
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

    def toPointCloud(self):
        pc = o3d.geometry.PointCloud()
        pc.points = o3d.utility.Vector3dVector(self.getPoints())
        pc.colors = o3d.utility.Vector3dVector(self.getColors())
        return pc


points = np.loadtxt("../data/lights/lights_4_upright_manual_selected.csv", delimiter=",")


lights = Lights()
for i in range(0, len(points)):
    lights.add(points[i], [1, 0, 0])


# np.savetxt("../data/lights/lights_4_upright_presorted.csv", npPoints, delimiter=",")

inputFile = "../data/point_clouds/decerto_choinka_4_upright.ply"
pointCloudData = PointCloudData.initFromFile(inputFile)
colorFiltered = NotBrownColorFilter().filter(pointCloudData)

print(lights.toPointCloud().points)
v = visualizerOf([], axis=True)

pcdRenderer = O3dRenderer(v)
circleRenderer = O3dRenderer(v)
savedBulbRendered = O3dRenderer(v)

# pcdPoints = np.zeros((0, 3))
pcdPoints = colorFiltered.npPoints
# pcdColor = np.zeros((0, 3))
pcdColor = colorFiltered.npColors


count = 1
r0 = 1
a0 = 10
z0 = 2
npCirclePoints = np.zeros((0, 3))
npCircleColors = np.zeros((0, 3))
npSavedPoints = np.zeros((0, 3))


def renderAll():
    pcdRenderer.render(pcdPoints, pcdColor)
    savedBulbRendered.render(lights.getPoints(), lights.getColors())
    circleRenderer.render(npCirclePoints, npCircleColors)


def cutPcdPoints():
    global pcdPoints
    global pcdColor

    pcdPoints = np.copy(colorFiltered.npPoints)
    pcdColor = np.copy(colorFiltered.npColors)
    for i in range(0, len(colorFiltered.npPoints)):
        z = colorFiltered.npPoints[i][2]
        if z > z0:
            pcdPoints[i] = [0, 0, 0]


def cutPcdPoints2():
    global pcdPoints
    global pcdColor

    # pcdPoints = np.zeros((0, 3))
    # pcdColor = np.zeros((0, 3))
    for i in range(0, len(colorFiltered.npPoints)):
        z = colorFiltered.npPoints[i][2]
        if z > 10:
            pcdPoints[i] = [0, 0, 0]


def calcPos(phi, r, z):
    x = r * math.sin(phi)
    y = r * math.cos(phi)

    return [x, y, z]


def updateCircle():
    global npCirclePoints
    global npCircleColors

    npCirclePoints = np.zeros((0, 3))
    npCircleColors = np.zeros((0, 3))
    for phi in np.arange(0, 2 * math.pi, 2 * math.pi / 200):
        x, y, z = calcPos(phi, r0, z0)

        npCirclePoints = np.append(npCirclePoints, [[x, y, z]], axis=0)
        npCircleColors = np.append(npCircleColors, [[0, 1, 0]], axis=0)

    x, y, z = calcPos(math.radians(a0), r0, z0)
    lb = LighBulb(0, [x, y, z], [0, 1, 0])
    npCirclePoints = np.append(npCirclePoints, lb.bulbPoints, axis=0)
    npCircleColors = np.append(npCircleColors, lb.bulbColors, axis=0)

    # cutPcdPoints()
    renderAll()


def save(vis):
    global npSavedPoints
    x, y, z = calcPos(a0 / 360, r0, z0)
    npSavedPoints = np.append(npSavedPoints, [[x, y, z]], axis=0)
    print(f"save: {x},{y},{z}")

    with open("../data/lights/lights_4_upright_program_save.csv", "a") as f:
        f.write("\n")
        f.write(f"{x},{y},{z}")

    False


def incrementZ0(vis):
    global z0
    z0 += 0.2
    print("z0", z0)
    updateCircle()
    return False


def decrementZ0(vis):
    global z0
    z0 -= 0.2
    print("z0", z0)
    updateCircle()
    return False


def incrementZ0By1(vis):
    global z0
    z0 += 1
    print("z0", z0)
    updateCircle()
    return False


def decrementZ0By1(vis):
    global z0
    z0 -= 1
    print("z0", z0)
    updateCircle()
    return False


def incrementR0(vis):
    global r0
    r0 += 0.2
    print("r0", r0)
    updateCircle()
    return False


def decrementR0(vis):
    global r0
    r0 -= 0.2
    print("r0", r0)
    updateCircle()
    return False


def incrementA0(vis):
    global a0
    a0 += 10
    print("a0", a0)
    updateCircle()
    return False


def decrementA0(vis):
    global a0
    a0 -= 10
    print("a0", a0)
    updateCircle()
    return False


updateCircle()

v.vis.register_key_callback(ord("Y"), incrementZ0)
v.vis.register_key_callback(ord("U"), decrementZ0)
v.vis.register_key_callback(ord("I"), incrementZ0By1)
v.vis.register_key_callback(ord("O"), decrementZ0By1)

v.vis.register_key_callback(ord("H"), incrementR0)
v.vis.register_key_callback(ord("J"), decrementR0)

v.vis.register_key_callback(ord("N"), incrementA0)
v.vis.register_key_callback(ord("M"), decrementA0)


v.vis.register_key_callback(ord("G"), save)


# while True:
#     # count = int(input("Liczba lampek do zapalenia: "))
# renderer.render(lights.getPointsCount(count), lights.getColorsCount(count))

#     time.sleep(0.05)
cutPcdPoints2()
renderAll()

v.show()
