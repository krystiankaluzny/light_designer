import numpy as np
import time
from renderer.rendererFactory import createRenderer

points = np.loadtxt("raw.txt", delimiter=",")
renderer = createRenderer()


colors = list()
colors.append([1.0, 0.0, 0.0])
colors.append([0.0, 1.0, 0.0])
colors.append([0.0, 0.0, 1.0])
colors.append([1.0, 1.0, 0.0])
colors.append([1.0, 0.0, 1.0])
colors.append([0.0, 1.0, 1.0])
colors.append([1.0, 0.0, 0.5])

npColors = np.zeros((len(points), 3))

for i in range(len(npColors)):
    segmentNumber = int(i / 10)
    colorIndex = segmentNumber % len(colors)
    npColors[i] = colors[colorIndex]


while True:
    renderer.render(points, npColors)
    time.sleep(0.05)
