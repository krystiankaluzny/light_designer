import math
import numpy as np
import open3d as o3d
import random
import sys

sys.path.append('../')
from renderer.visualizer import visualizerOf

# spiral config
# rozciągłość x-y spirali https://pl.wikipedia.org/wiki/Spirala_Archimedesa
a = 1 / 200

# nachylenie spirali - i mniejsza wartość tym mniejszy skok, https://en.wikipedia.org/wiki/Conical_spiral
m = 1 / 100

expectedHeight = 1.5
expectedRadius = 1.25 / 2

angleStep = 2 * math.pi / 360 / 2
maxAngle = 2 * math.pi * 20
# maxAngle = 0


# generate spiral in high resolution
z0 = expectedHeight


def curveLen(array):
    length = 0

    if len(array) > 1:
        for i in range(1, len(array)):
            length += math.dist(array[i - 1], array[i])

    return length


def calculateConeSpiralPoint(phi):
    x = a * phi * math.sin(phi)
    y = a * phi * math.cos(phi)
    z = z0 - m * phi
    r = a * phi
    return x, y, z, r


def testConeConfigParams():
    array = np.array([[0, 0, z0]])
    i = 0
    r = 0
    lastZAt0 = z0
    for phi in np.arange(0, maxAngle, angleStep):
        x, y, z, r = calculateConeSpiralPoint(phi)

        # array[i] = [x, y, z]
        array = np.append(array, [[x, y, z]], axis=0)
        i += 1

        if (phi % (2 * math.pi)) < 0.001:
            print("phi", phi, "z", z, "diff", lastZAt0 - z)
            lastZAt0 = z

        if z < 0:
            print("z<0", phi)
            break

        if r > expectedRadius:
            print("r > expectedRadius", phi)
            break

    # array = array.reshape(i, 3)
    length = curveLen(array)
    segmentLen = length / 502

    print("L", length, "r", r, "segmentLen", segmentLen)
    return array


def findConePoints(expectedSegmentLen):
    segmentArray = np.array([[0, 0, z0]])
    points = np.array([[0, 0, z0]])
    i = 0
    totalLenght = 0

    for phi in np.arange(0, maxAngle, angleStep / 20):
        x, y, z, r = calculateConeSpiralPoint(phi)

        segmentArray = np.append(segmentArray, [[x, y, z]], axis=0)
        segmentLen = curveLen(segmentArray)

        if segmentLen > expectedSegmentLen:
            totalLenght += segmentLen
            points = np.append(points, [[x, y, z]], axis=0)
            segmentArray = np.array([[x, y, z]])
            print(i, segmentLen)
            i += 1

        if z < 0:
            print("z<0", phi)
            break

        if r > expectedRadius:
            print("r > expectedRadius", r, "phi", phi)
            break

        if(len(points) == 500):
            print("500")
            break

    print("P Len", len(points), "totalLenght", totalLenght)

    return points


def testAndDrow():
    points = testConeConfigParams()
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    pcd.paint_uniform_color([0, 0, 1])
    v = visualizerOf([pcd], axis=False)
    v.show()


def findAndDrow():
    points = findConePoints(0.0779439968973369)
    np.savetxt("../data/cone_test/cone_test_points_2.csv", points, delimiter=",")
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    pcd.paint_uniform_color([0, 0, 1])
    v = visualizerOf([pcd], axis=False)
    v.show()


def rand(factor):
    return random.uniform(-expectedRadius / factor, +expectedRadius / factor)


def addPositionNoise(noiseLevel):
    points = np.loadtxt("../data/cone_test/cone_test_points_2.csv", delimiter=",")
    for i, p in enumerate(points):
        points[i] = [p[0] + rand(noiseLevel), p[1] + rand(noiseLevel), p[2] + rand(noiseLevel)]

    np.savetxt(f"../data/cone_test/cone_test_points_rand_{noiseLevel}.csv", points, delimiter=",")
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    pcd.paint_uniform_color([0, 0, 1])
    v = visualizerOf([pcd], axis=False)
    v.show()


# testAndDrow()
# findAndDrow()
addPositionNoise(33)
