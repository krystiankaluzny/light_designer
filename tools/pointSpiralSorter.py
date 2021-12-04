import numpy as np
import time
import math
import sys
import matplotlib.pyplot as plt
from dataclasses import dataclass

sys.path.append('../')

from renderer.o3dRenderer import O3dRenderer
from renderer.visualizer import visualizerOf


points = np.loadtxt("../data/cone_test/cone_test_points_rondomized.csv", delimiter=",")

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


zMin = points.min(axis=0)[2]
zMax = points.max(axis=0)[2]

sliceCount = 20
sliceWith = zMax / sliceCount


pointSlices = dict()

for i in range(0, len(points)):
    p = points[i]
    z = p[2]
    sliceId = int(z / sliceWith)

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


v = visualizerOf([], axis=True)
renderer = O3dRenderer(v)

# while True:
#     renderer.render(npPoints, npColors)

#     time.sleep(0.05)


color = [0.8, 0.1, 0.2]
step = 1
start = 0
stop = 0


while True:
    colors = ColorBuilder(npPoints).inIndexRange(color, start, stop).build()
    renderer.render(npPoints, colors)

    stop += step
    if stop >= len(npPoints):
        stop = 0

    time.sleep(0.05)


while True:
    colors = ColorBuilder(npPoints).inIndexRange(color, start, stop).build()
    renderer.render(npPoints, colors)

    stop += step
    if stop >= len(npPoints):
        stop = 0

    time.sleep(0.05)
