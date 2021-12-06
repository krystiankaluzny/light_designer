import numpy as np
import time
import math
import sys
from PIL import Image
from rendererFactory import createRenderer


points = np.loadtxt("data/cone_test/cone_test_points_rand_15.csv", delimiter=",")

renderer = createRenderer()


def colorInRange(points, color, start, stop):
    colors = np.zeros((len(points), 3))~
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


img = Image.open('data/images/decerto_flag.jpg')
ary = np.array(img)

npPoints = np.zeros((0, 3))
npColors = np.zeros((0, 3))

for i in range(len(ary)):
    for j in range(len(ary[i])):
        npPoints = np.append(npPoints, [[i, j, 0]], axis=0)
        npColors = np.append(npColors, [[ary[i][j][0] / 256, ary[i][j][1] / 255, ary[i][j][2] / 256]], axis=0)


while True:
    renderer.render(npPoints, npColors)
    time.sleep(0.05)
