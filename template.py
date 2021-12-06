import numpy as np
import time
from renderer.rendererFactory import createRenderer

# 1. wczytaj pozycja lampek choinkowych
points = np.loadtxt("raw.txt", delimiter=",")
# 2. utówrz renderer
renderer = createRenderer()

# 3. zaimplementów swój program
colors = list()
colors.append([1.0, 0.0, 0.0])
colors.append([0.0, 1.0, 0.0])
colors.append([0.0, 0.0, 1.0])
colors.append([1.0, 1.0, 0.0])
colors.append([1.0, 0.0, 1.0])
colors.append([0.0, 1.0, 1.0])
colors.append([1.0, 0.0, 0.5])


length = 0

while True:
    npColors = np.zeros((len(points), 3))

    for i in range(length):
        colorIndex = i % len(colors)
        npColors[i] = colors[colorIndex]

    length += 1
    if length >= len(points):
        length = 0

    # 4. wyślij dane na choinkę lub symulator
    renderer.render(points, npColors)
    time.sleep(0.05)
