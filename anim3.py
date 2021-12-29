import numpy as np
import time
from renderer.rendererFactory import createRenderer

# Kolory przmieszczające się od góry do dołu

# 1. wczytaj pozycja lampek choinkowych
points = np.loadtxt("raw.txt", delimiter=",")
# 2. utówrz renderer
renderer = createRenderer()

# 3. zaimplementów swój program
colors = list()
colors.append([255, 0.0, 0.0])
colors.append([125, 60, 152])
colors.append([255, 255, 0.0])
colors.append([88, 214, 141])
colors.append([127, 140, 141])
colors.append([220, 118, 51])
colors.append([113, 125, 126])
colors.append([0.0, 0.0, 255])
colors.append([255, 0.0, 255])
colors.append([255, 0.0, 128])
colors.append([0.0, 255, 0.0])
colors.append([0.0, 255, 255])
colors.append([93, 173, 226])
colors.append([240, 178, 122])

zMin = points.min(axis=0)[2]
zMax = points.max(axis=0)[2]
zH = zMax - zMin
bandHight = zH / len(colors)

bandsTop = zMin
step = (zMax - zMin) / 30

# UP or DOWN
currentDirection = 'UP'

while True:
    npColors = np.zeros((len(points), 3))

    for i in range(0, len(points)):
        z = points[i][2]

        for j in range(0, len(colors)):
            if z < (bandsTop - j * bandHight) and z >= (bandsTop - (j + 1) * bandHight):
                npColors[i] = colors[j]

    # 4. wyślij dane na choinkę lub symulator
    renderer.render256(points, npColors)

    if currentDirection == 'UP':
        bandsTop += step
        if bandsTop >= zMax + zH:
            currentDirection = 'DOWN'
    elif currentDirection == 'DOWN':
        bandsTop -= step
        if bandsTop <= zMin:
            currentDirection = 'UP'
