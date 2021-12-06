import numpy as np
import open3d as o3d
import colorsys
import sys

from plyfile import PlyData
from dataclasses import dataclass

sys.path.append('../')
from renderer.visualizer import visualizerOf


@dataclass
class PointCloudData(object):
    npPoints: np.ndarray
    npColors: np.ndarray

    @staticmethod
    def initFromFile(plyFile):
        plyData = PlyData.read(plyFile)
        elements = plyData.elements[0]
        elementSize = len(elements)
        npPoints = np.zeros((elementSize, 3))
        npColors = np.zeros((elementSize, 3))

        for i, e in enumerate(elements):
            npPoints[i] = [e[0], e[1], e[2]]
            npColors[i] = [e[6] / 256, e[7] / 256, e[8] / 256]

        return PointCloudData(npPoints, npColors)

    def toPointCloud(self):
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(self.npPoints)
        pcd.colors = o3d.utility.Vector3dVector(self.npColors)
        return pcd


class ColorFilter(object):

    def filter(self, pointCloudData: PointCloudData):
        npPoints = np.zeros((len(pointCloudData.npPoints), 3))
        npColors = np.zeros((len(pointCloudData.npColors), 3))

        idx = 0
        for i, c in enumerate(pointCloudData.npColors):
            hlsColor = colorsys.rgb_to_hls(c[0], c[1], c[2])
            if self.checkHls(hlsColor):
                npPoints[idx] = pointCloudData.npPoints[i]
                npColors[idx] = c
                idx += 1

        npPoints = npPoints[~np.all(npPoints == 0, axis=1)]
        npColors = npColors[~np.all(npColors == 0, axis=1)]
        return PointCloudData(npPoints, npColors)

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

class NotBrownColorFilter(ColorFilter):

    def checkHls(self, hlsColor):
        h = hlsColor[0] * 360
        return h < 10 or h > 80
