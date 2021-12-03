import numpy as np
import open3d as o3d
import colorsys
import sys
import matplotlib.pyplot as plt
from plyfile import PlyData
from typing import Mapping
from dataclasses import dataclass

sys.path.append('../')
from renderer.visualizer import visualizerOf


@dataclass
class PointCloudData(object):
    npPoints: np.ndarray
    npColors: np.ndarray

    @staticmethod
    def initFromFile(plyFile):
        plyData = PlyData.read(inputFile)
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

    @staticmethod
    def filter(pointCloudData: PointCloudData):
        npPoints = np.zeros((len(pointCloudData.npPoints), 3))
        npColors = np.zeros((len(pointCloudData.npColors), 3))

        idx = 0
        for i, c in enumerate(pointCloudData.npColors):
            hlsColor = colorsys.rgb_to_hls(c[0], c[1], c[2])
            if ColorFilter.isLighted(hlsColor) and ColorFilter.isLightBlue(hlsColor):
                npPoints[idx] = pointCloudData.npPoints[i]
                npColors[idx] = c
                idx += 1

        npPoints = npPoints[~np.all(npPoints == 0, axis=1)]
        npColors = npColors[~np.all(npColors == 0, axis=1)]
        return PointCloudData(npPoints, npColors)

    @staticmethod
    def isLighted(hlsColor):
        return hlsColor[1] > 0.60
        return True

    @staticmethod
    def isLightBlue(hlsColor):
        h = hlsColor[0] * 360
        # return True
        return h > 160 and h < 220


class NoiseFilter(object):

    @staticmethod
    def filter(pcd: PointCloudData, labels: np.ndarray):
        isLabel = np.greater_equal(labels, 0)
        labels = labels[isLabel]
        npPoints = pcd.npPoints[isLabel]
        npColors = pcd.npColors[isLabel][:, :3]
        return PointCloudData(npPoints, npColors), labels


class Colorizer(object):

    @staticmethod
    def colorize(pcd: PointCloudData, labels: np.ndarray):
        maxLabel = labels.max()
        print(maxLabel)
        colors = plt.get_cmap("tab20")(labels / (maxLabel if maxLabel > 0 else 1))

        isLabel = np.greater_equal(labels, 0)
        npPoints = pcd.npPoints[isLabel]
        npColors = colors[isLabel][:, :3]
        return PointCloudData(npPoints, npColors)

    @staticmethod
    def colorizeFirstLabels(pcd: PointCloudData, labels: np.ndarray, numOfLabelsToColorize=10):
        maxLabel = labels.max()
        print(maxLabel)
        colors = plt.get_cmap("tab20")(labels / (maxLabel if maxLabel > 0 else 1))
        colors[labels > numOfLabelsToColorize] = 0

        npPoints = pcd.npPoints
        npColors = colors[:, :3]
        return PointCloudData(npPoints, npColors)


@dataclass
class SinglePointCluster(object):
    id: int
    points: list
    colors: list
    center: np.ndarray = np.empty(1)
    colorCenter: np.ndarray = np.empty(1)

    def add(self, point, color):
        self.points.append(point)
        self.colors.append(color)

    def calcCenter(self):
        self.center = np.mean(np.array(self.points), axis=0)
        self.colorCenter = np.mean(np.array(self.colors), axis=0)


@dataclass
class PointClusters(object):
    clusters: Mapping[int, SinglePointCluster]

    @staticmethod
    def create(pcd: PointCloudData, labels: np.ndarray):

        clusters = dict()

        for i in range(0, len(labels)):
            id = labels[i]
            point = pcd.npPoints[i]
            color = pcd.npColors[i]
            if id in clusters:
                cluster = clusters[id]
            else:
                cluster = SinglePointCluster(id, [], [])
                clusters[id] = cluster

            cluster.add(point, color)

        return PointClusters(clusters)

    def calculate(self):
        for key in self.clusters:
            self.clusters[key].calcCenter()

    def toPointCloud(self):
        elementSize = len(self.clusters)
        npPoints = np.zeros((elementSize, 3))
        npColors = np.zeros((elementSize, 3))

        for key in self.clusters:
            singlePointCluster = self.clusters[key]
            npPoints[key] = singlePointCluster.center
            npColors[key] = singlePointCluster.colorCenter

        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(npPoints)
        pcd.colors = o3d.utility.Vector3dVector(npColors)
        return pcd

    def toCenterMap(self):
        centers = dict()

        for key in self.clusters:
            singlePointCluster = self.clusters[key]
            centers[key] = singlePointCluster.center
        return centers

    def toCenters(self):
        elementSize = len(self.clusters)
        npPoints = np.zeros((elementSize, 3))

        for key in self.clusters:
            singlePointCluster = self.clusters[key]
            npPoints[key] = singlePointCluster.center

        return npPoints


# inputFile = "point_clouds/test9.1.ply"
inputFile = "../data/point_clouds/decerto_choinka_2.ply"
pointCloudData = PointCloudData.initFromFile(inputFile)
colorFiltered = ColorFilter.filter(pointCloudData)


pcd = colorFiltered.toPointCloud()
labels = np.array(pcd.cluster_dbscan(eps=0.04, min_points=7))

filtered, labels = NoiseFilter.filter(colorFiltered, labels)
# colorized = colorFiltered
colorized = filtered
colorized = Colorizer.colorize(filtered, labels)
# colorized = Colorizer.colorizeFirstLabels(colorized, labels, 20)

# print(len(filtered.npPoints))
# print(len(filtered.npColors))
pointClusters = PointClusters.create(colorized, labels)
pointClusters.calculate()
clustered = pointClusters.toPointCloud()
print(len(pointClusters.toCenterMap()))
# Zapis
np.savetxt("../data/lights/lights_1.csv", pointClusters.toCenters(), delimiter=",")

# show oryginal points
# v = visualizerOf([pointCloudData.toPointCloud()], axis=False)

# show all points
# v = visualizerOf([colorized.toPointCloud()], axis=False)

# show cluster centers
# v = visualizerOf([pointClusters.toPointCloud()], axis=False)
# v.show()


