import numpy as np
import open3d as o3d
import colorsys
import sys
import datetime

from plyfile import PlyData, PlyElement
from dataclasses import dataclass

sys.path.append('../')


@dataclass
class PointCloudData(object):
    element: PlyElement
    elementSize: int
    npPoints: np.ndarray
    npColors: np.ndarray

    @staticmethod
    def initFromFile(plyFile):
        print(datetime.datetime.now(), "PointCloudData: start reading plyFile")
        plyData = PlyData.read(plyFile)
        element = plyData.elements[0]
        elementSize = len(element)
        print(datetime.datetime.now(), "PointCloudData: finished reading plyFile, size", elementSize)
        return PointCloudData(element, elementSize, [], [])

    def filter(self, filters: list):
        start = datetime.datetime.now()
        d1 = start
        print(datetime.datetime.now(), "PointCloudData: start filter")
        tmpPoints = np.empty((self.elementSize, 3))
        tmpColors = np.empty((self.elementSize, 3))
        tmpSize = 0

        for i, e in enumerate(self.element):
            x = e[0]
            y = e[1]
            z = e[2]
            r = e[6] / 256
            g = e[7] / 256
            b = e[8] / 256

            if i % 100000 == 0:
                d2 = datetime.datetime.now()
                print(datetime.datetime.now(), "PointCloudData: i", i, "elementSize",
                      self.elementSize, "progress", i / self.elementSize * 100, "duration", d2 - d1)
                d1 = d2

            add = True

            for f in filters:
                if not f.filter(i, x, y, z, r, g, b):
                    add = False
                    break

            if add:
                tmpPoints[tmpSize] = [x, y, z]
                tmpColors[tmpSize] = [r, g, b]
                tmpSize = tmpSize + 1

        print(datetime.datetime.now(), "PointCloudData: start slicing to ", tmpSize, "from", self.elementSize)

        if len(filters) > 0:
            self.npPoints = tmpPoints[0:tmpSize]
            self.npColors = tmpColors[0:tmpSize]
        else:
            self.npPoints = tmpPoints
            self.npColors = tmpColors

        print(datetime.datetime.now(), "PointCloudData: finished slicing to ", tmpSize, "from", self.elementSize)
        finish = datetime.datetime.now()
        print(datetime.datetime.now(), "PointCloudData: finished filter duration:", finish - start)

    def toPointCloud(self):
        print(datetime.datetime.now(), "PointCloudData: start toPointCloud")
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(self.npPoints)
        pcd.colors = o3d.utility.Vector3dVector(self.npColors)
        print(datetime.datetime.now(), "PointCloudData: finished toPointCloud")
        return pcd


class PointCloudDataFilter(object):

    def filter(self, index, x, y, z, r, g, b) -> bool:
        pass


class ColorFilter(PointCloudDataFilter):

    def filter(self, index, x, y, z, r, g, b):
        hlsColor = colorsys.rgb_to_hls(r, g, b)
        return self.checkHls(hlsColor)

    def checkHls(self, hlsColor):
        return True


class BlueColorFilter(ColorFilter):

    def checkHls(self, hlsColor):
        return self.isLighted(hlsColor) and self.isLightBlue(hlsColor)

    def isLighted(sefl, hlsColor):
        return hlsColor[1] > 0.70

    def isLightBlue(self, hlsColor):
        h = hlsColor[0] * 360
        return h > 160 and h < 200


class LightedColorFilter(ColorFilter):

    def checkHls(self, hlsColor):
        return self.isLighted(hlsColor)

    def isLighted(sefl, hlsColor):
        return hlsColor[1] > 0.75


class NotBrownColorFilter(ColorFilter):

    def checkHls(self, hlsColor):
        h = hlsColor[0] * 360
        return h < 10 or h > 80
