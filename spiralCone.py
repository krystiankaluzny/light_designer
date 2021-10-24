import math
import numpy as np
import open3d as o3d
from visualizer import *


a = 1 / 60
m = 2.3
k = 1.35

expectedHeight = 1.5
expectedRadius = 1.25 / 2

angleStep = 2 * math.pi / 360 / 2
# maxAngle = 2 * math.pi * 10
maxAngle = 0

z0 = expectedHeight

array = np.array([[0, 0, z0]])

i = 0
r = 0
for phi in np.arange(0, maxAngle, angleStep):
    x = a * phi * math.sin(phi)
    y = a * phi * math.cos(phi)
    z = z0 - k * m * a * phi
    r = a * phi

    # array[i] = [x, y, z]
    array = np.append(array, [[x, y, z]], axis=0)
    i += 1

    if z < 0:
        print("z<0", phi)
        break

    if r > expectedRadius:
        print("r > expectedRadius", phi)
        break

# array = array.reshape(i, 3)


def curveLen(array):
    length = 0

    if len(array) > 1:
        for i in range(1, len(array)):
            length += math.dist(array[i - 1], array[i])

    return length


length = curveLen(array)


partLen = length / 502

print("L", length, "r", r, "partLen", partLen)


partArray = np.array([[0, 0, z0]])
points = np.array([[0, 0, z0]])
i = 0
tL = 0
for phi in np.arange(0, maxAngle, angleStep / 20):
    x = a * phi * math.sin(phi)
    y = a * phi * math.cos(phi)
    z = z0 - k * m * a * phi
    r = a * phi

    # array[i] = [x, y, z]

    partArray = np.append(partArray, [[x, y, z]], axis=0)
    l = curveLen(partArray)

    if l > partLen:
        tL += l
        points = np.append(points, [[x, y, z]], axis=0)
        partArray = np.array([[x, y, z]])
        print(i, l)
        i += 1

    if z < 0:
        print("z<0", phi)
        break

    if r > expectedRadius:
        print("r > expectedRadius", phi)
        break

    if(len(points) == 500):
        print("500")
        break

points = np.flip(points, axis=0)
pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(array)

print("P Len", len(points), "tL", tL)

points = np.loadtxt("point_clouds/cone_test_points.csv", delimiter=",")


pc2 = o3d.geometry.PointCloud()
pc2.points = o3d.utility.Vector3dVector(points)
pc2.paint_uniform_color([0, 0, 1])
# arrow = o3d.geometry.TriangleMesh.create_arrow()

v = visualizerOf([pc2])
# v.show()

for i in range(0, len(points)):
    pc2.colors[i] = [i / len(points), i / len(points), 0]
    v.updateGeometryAndRefresh([pc2])

v.show()
# np.savetxt("point_clouds/cone_test_points.csv", points, delimiter=",")
