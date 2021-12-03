import numpy as np
import open3d as o3d
from renderer.renderer import Renderer
from renderer.visualizer import visualizerOf


class O3dRenderer(Renderer):

    def __init__(self, visualizer):
        if visualizer:
            self.__v = visualizer
        else:
            self.__v = visualizerOf([])
        self.__init = False

    def render(self, points: np.ndarray, colors: np.ndarray):
        if not self.__init:
            self.__pc = o3d.geometry.PointCloud()
            self.__pc.points = o3d.utility.Vector3dVector(points)
            self.__pc.colors = o3d.utility.Vector3dVector(colors)
            self.__v.addGeometry([self.__pc])
            self.__v.updateGeometryAndRefresh([self.__pc])
            self.__init = True
        else:
            self.__pc.points = o3d.utility.Vector3dVector(points)
            self.__pc.colors = o3d.utility.Vector3dVector(colors)
            self.__v.updateGeometryAndRefresh([self.__pc])
