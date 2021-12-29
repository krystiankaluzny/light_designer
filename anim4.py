import numpy as np
import time
import random
from renderer.rendererFactory import createRenderer
from dataclasses import dataclass

# Kolory przmieszczające się od góry zapętlone

# 1. wczytaj pozycja lampek choinkowych
points = np.loadtxt("raw.txt", delimiter=",")
# 2. utówrz renderer
renderer = createRenderer()

# 3. zaimplementów swój program


zMin = points.min(axis=0)[2]
zMax = points.max(axis=0)[2]
zH = zMax - zMin

bandsTop = zMin
step = (zMax - zMin) / 30


@dataclass
class Band(object):
    zFrom: float
    zTo: float
    color: list

    def contains(self, z):
        return z >= self.zFrom and z < self.zTo

    def moveBy(self, step):
        self.zFrom += step
        self.zTo += step

class AllBand(object):

    def __init__(self, size, bandHight):
        self.bands = []
        self.bandHight = bandHight
        for i in range(size):
            self.bands.append(Band(bandsTop - (i + 1) * self.bandHight, bandsTop - (i) * self.bandHight, self.randomColor()))

    def randomColor(self):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        return [r, g, b]

    def getColor(self, x):
        for b in self.bands:
            if b.contains(x):
                return b.color

        return [0, 0, 0]

    def moveBy(self, step):
        for b in self.bands:
            b.moveBy(step)

        if self.bands[0].zFrom > zMax:
            first = self.bands.pop(0)
            first.zFrom = self.bands[-1].zFrom - self.bandHight
            first.zTo = self.bands[-1].zFrom
            self.bands.append(first)


allBands = AllBand(100, zH / 10)

while True:
    npColors = np.zeros((len(points), 3))

    for i in range(0, len(points)):
        z = points[i][2]
        npColors[i] = allBands.getColor(z)

    # 4. wyślij dane na choinkę lub symulator
    renderer.render256(points, npColors)

    allBands.moveBy(step)
