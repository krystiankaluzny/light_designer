import open3d as o3d
import numpy as np


def change_background_to_black(vis):
    opt = vis.get_render_option()
    opt.background_color = np.asarray([0, 0, 0])
    return False


def change_background_to_white(vis):
    opt = vis.get_render_option()
    opt.background_color = np.asarray([1, 1, 1])
    return False


def visualize(pointClouds):
    key_to_callback = {}
    key_to_callback[ord("B")] = change_background_to_black
    key_to_callback[ord("W")] = change_background_to_white
    o3d.visualization.draw_geometries_with_key_callbacks(pointClouds, key_to_callback)
