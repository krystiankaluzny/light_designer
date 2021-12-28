import numpy as np
import open3d as o3d
import sys
import matplotlib.pyplot as plt
import datetime

from typing import Mapping
from dataclasses import dataclass

sys.path.append('../')
from renderer.visualizer import visualizerOf
from tools.pointCloudData import PointCloudData, PointCloudDataFilter, BlueColorFilter, NotBrownColorFilter, LightedColorFilter


class DefaultFilter(PointCloudDataFilter):
    def filter(self, index, x, y, z, r, g, b) -> bool:
        return True

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
# inputFile = "../data/point_clouds/decerto_choinka_4_upright.ply"
startLoading = datetime.datetime.now()
inputFile = "/home/kkaluzny/Documents/decerto_choinka/ch_07_exported_filtered.ply"
pointCloudData = PointCloudData.initFromFile(inputFile)
pointCloudData.filter([LightedColorFilter()])

finishLoading = datetime.datetime.now()
print('Loading duration', finishLoading - startLoading)
colorFiltered = pointCloudData


# pcd = colorFiltered.toPointCloud()
# labels = np.array(pcd.cluster_dbscan(eps=0.04, min_points=7))

# filtered, labels = NoiseFilter.filter(colorFiltered, labels)
# colorized = colorFiltered
# colorized = filtered
# colorized = Colorizer.colorize(filtered, labels)
# colorized = Colorizer.colorizeFirstLabels(colorized, labels, 20)

# print(len(filtered.npPoints))
# print(len(filtered.npColors))
# pointClusters = PointClusters.create(colorized, labels)
# pointClusters.calculate()
# clustered = pointClusters.toPointCloud()
# print(len(pointClusters.toCenterMap()))
# Zapis
# np.savetxt("../data/lights/ch_07_exported_filtered.csv", pointClusters.toCenters(), delimiter=",")

# show oryginal points
v = visualizerOf([pointCloudData.toPointCloud()], {'axis': False, 'pointSize': 2})

# show all points
# v = visualizerOf([colorized.toPointCloud()], axis=True)

# show cluster centers
# v = visualizerOf([pointClusters.toPointCloud()], axis=False)
v.show()
