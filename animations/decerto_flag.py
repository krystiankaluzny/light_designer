import numpy as np
import time
import math
import sys
from PIL import Image

sys.path.append('../')
from renderer.o3dRenderer import O3dRenderer
from renderer.visualizer import visualizerOf

# painter = Painter(O3dRenderer())
# painter.show()
# v.show()


points = np.loadtxt("../data/cone_test/cone_test_points_rand_15.csv", delimiter=",")


v = visualizerOf([], axis=False)
renderer = O3dRenderer(v)


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


img = Image.open('../data/images/decerto_flag_2.jpg')
ary = np.array(img)
print(ary[0])
# Split the three channels
r, g, b = np.split(ary, 3, axis=2)
r = r.reshape(-1)
g = g.reshape(-1)
b = b.reshape(-1)

# Standard RGB to grayscale
bitmap = list(map(lambda x: 0.299 * x[0] + 0.587 * x[1] + 0.114 * x[2], zip(r, g, b)))
bitmap = np.array(bitmap).reshape([ary.shape[0], ary.shape[1]])
bitmap = np.dot((bitmap > 128).astype(float), 255)
im = Image.fromarray(bitmap.astype(np.uint8))
im.save('../data/images/road.bmp')

npPoints = np.zeros((0, 3))
npColors = np.zeros((0, 3))

for i in range(len(ary)):
    for j in range(len(ary[i])):
        npPoints = np.append(npPoints, [[i, j, 0]], axis=0)
        npColors = np.append(npColors, [[ary[i][j][0] / 256, ary[i][j][1] / 255, ary[i][j][2] / 256]], axis=0)


while True:

    renderer.render(npPoints, npColors)
    time.sleep(0.05)


# v.show()
# painter = Painter(O3dRenderer())
# painter.show()
# v.show()
