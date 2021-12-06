import numpy as np
import random

class LighBulb(object):

    def __init__(self, index, radius, center, color):
        self.index = index
        self.center = center
        self.color = color
        self.radius = radius
        self.bulbPoints = self.generateBulb(center)
        self.bulbColors = np.zeros((len(self.bulbPoints), 3))
        self.setColor(color)

    def generateBulb(self, center):
        npPoints = np.zeros((0, 3))
        npPoints = np.append(npPoints, [center], axis=0)
        i = 0
        while i < 50:
            p = self.randPoint(center)
            if p is not None:
                npPoints = np.append(npPoints, [p], axis=0)
                i += 1

        return npPoints

    def randPoint(self, center):
        r = self.radius
        dx = random.uniform(-r, +r)
        dy = random.uniform(-r, +r)
        dz = random.uniform(-r, +r)
        if pow(dx, 2) + pow(dy, 2) + pow(dz, 2) <= pow(r, 2):
            return [center[0] + dx, center[1] + dy, center[2] + dz]

        return None

    def setColor(self, color):
        self.color = color
        for i in range(len(self.bulbColors)):
            self.bulbColors[i] = color


class Lights(object):

    def __init__(self, radius):
        self.lastIndex = -1
        self.radius = radius
        self.bulbs = list()

    @staticmethod
    def createLights(radius, points):
        lights = Lights(radius)
        for i in range(0, len(points)):
            lights.add(points[i], [1, 0, 0])
        return lights

    def __len__(self):
        return len(self.bulbs)

    def __getitem__(self, key):
        return self.bulbs[key]

    def add(self, center, color):
        self.lastIndex += 1
        self.bulbs.append(LighBulb(self.lastIndex, self.radius, center, color))

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
