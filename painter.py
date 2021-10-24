import math
import numpy as np
import open3d as o3d
from renderer.renderer import Renderer

class Painter(object):

    def __init__(self, renderer: Renderer):
        self.__points = np.loadtxt("point_clouds/cone_test_points.csv", delimiter=",")
        self.__colors = np.zeros((len(self.__points), 3))
        self.__renderer = renderer

    def __len__(self):
        return len(self.__colors)

    def __getitem__(self, index):
        return self.__colors(index)

    def __setitem__(self, index, value):
        self.__colors[index] = value

    def show(self):
        self.__renderer.render(self.__points, self.__colors)
