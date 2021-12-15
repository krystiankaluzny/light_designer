import numpy as np
import time
import math
import random
from PIL import Image
from renderer.rendererFactory import createRenderer


points = np.loadtxt("raw.txt", delimiter=",")

renderer = createRenderer()


zMin = points.min(axis=0)[2]
zMax = points.max(axis=0)[2]
zH = (zMax - zMin)


img = Image.open('data/images/decerto_flag.jpg')
ary = np.array(img)
width = len(ary)
height = len(ary[0])

print(height)


def zToJ(z):
    return int((z - zMin) / zH * height * 1.2)


def xyToI(x, y, angleOffset):
    angle = math.degrees(math.atan2(y, x))
    if angle < 0:
        angle += 360

    angle += angleOffset
    angle = angle % 360

    return int(angle / 180 * width)


def calcColors(angleOffset):
    colors = np.zeros((len(points), 3))

    for index in range(len(points)):
        p = points[index]
        i = xyToI(p[0], p[1], angleOffset)
        j = zToJ(p[2])
        if i >= 0 and j >= 0 and i < width and j < height:
            colors[index] = [ary[i][j][0], ary[i][j][1], ary[i][j][2]]
        else:
            colors[index] = [0, 0, 0]

    return colors


angleStep = 10
currentAngleOffset = 0

while True:
    renderer.render256(points, calcColors(currentAngleOffset))
    currentAngleOffset += angleStep
    time.sleep(0.05)
