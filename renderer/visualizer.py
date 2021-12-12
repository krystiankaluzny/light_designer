import open3d as o3d
import open3d.visualization as o3dv
import numpy as np
import os.path
from typing import List

class Visualizer(object):

    def __init__(self, vis: o3dv.Visualizer, config: dict):
        self.vis = vis
        self.config = config

    def addGeometry(self, geometries: List[o3d.geometry.Geometry]):
        for g in geometries:
            self.vis.add_geometry(g)

    def updateGeometry(self, geometries: List[o3d.geometry.Geometry]):
        for g in geometries:
            self.vis.update_geometry(g)

    def updateGeometryAndRefresh(self, geometries: List[o3d.geometry.Geometry]):
        for g in geometries:
            self.vis.update_geometry(g)
        self.vis.poll_events()
        self.vis.update_renderer()

    def __initCamera(self):
        vc: o3dv.ViewControl = self.vis.get_view_control()
        vc.set_front([0, -1, 0.2])

    def show(self):
        self.__initCamera()

        self.vis.run()  # until user presses "q" to terminate
        self.vis.destroy_window()


def visualizerOf(geometries: List[o3d.geometry.Geometry], config):
    vis = o3dv.VisualizerWithKeyCallback()
    vis.register_key_callback(ord("B"), __changeBackgroundToBlack)
    vis.register_key_callback(ord("W"), __changeBackgroundToWhite)
    vis.register_key_callback(ord("Q"), __quit)
    vis.create_window(config.get('windowsName', 'Test'))

    if config.get('axis', False):
        for axis in __createAxis(config):
            vis.add_geometry(axis)

    opt = vis.get_render_option()
    opt.point_size = config.get('pointSize', 8.0)
    v = Visualizer(vis, config)
    v.addGeometry(geometries)
    return v


def visualizerWithEditingOf(geometries: List[o3d.geometry.Geometry], config):
    vis = o3dv.VisualizerWithEditing()
    vis.create_window("Test")

    if config['axis']:
        for axis in __createAxis():
            vis.add_geometry(axis)

    v = Visualizer(vis)
    v.addGeometry(geometries)
    return v


def __changeBackgroundToBlack(vis):
    opt = vis.get_render_option()
    opt.background_color = np.asarray([0, 0, 0])
    return False


def __changeBackgroundToWhite(vis):
    opt = vis.get_render_option()
    opt.background_color = np.asarray([1, 1, 1])
    return False


def __quit(vis):
    vis.destroy_window()
    return False


def __text3D(text, config, pos, direction=None, degree=0.0, density=10, font_size=12) -> o3d.geometry.PointCloud():
    """
    Generate a 3D text point cloud used for visualization.
    :param text: content of the text
    :param pos: 3D xyz position of the text upper left corner
    :param direction: 3D normalized direction of where the text faces
    :param degree: in plane rotation of text
    :param font: Name of the font - change it according to your system
    :param font_size: size of the font
    :return: o3d.geoemtry.PointCloud object
    """

    font = config.get('axisFontLocation', '/usr/share/fonts/truetype/freefont/FreeMono.ttf')
    if not os.path.exists(font):
        print('Font location not exists', font)
        return o3d.geometry.PointCloud()

    font_size = config.get('axisFontSize', 12)
    if direction is None:
        direction = (0., 0., 1.)

    from PIL import Image, ImageFont, ImageDraw
    from pyquaternion import Quaternion

    font_obj = ImageFont.truetype(font, font_size * density)
    font_dim = font_obj.getsize(text)

    img = Image.new('RGB', font_dim, color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw.text((0, 0), text, font=font_obj, fill=(0, 0, 0))
    img = np.asarray(img)
    img_mask = img[:, :, 0] < 128
    indices = np.indices([*img.shape[0:2], 1])[:, img_mask, 0].reshape(3, -1).T

    pcd = o3d.geometry.PointCloud()
    pcd.colors = o3d.utility.Vector3dVector(img[img_mask, :].astype(float) / 255.0)
    pcd.points = o3d.utility.Vector3dVector(indices / 200.0 / density)

    raxis = np.cross([0.0, 0.0, 1.0], direction)
    if np.linalg.norm(raxis) < 1e-6:
        raxis = (0.0, 0.0, 1.0)
    trans = (Quaternion(axis=raxis, radians=np.arccos(direction[2])) *
             Quaternion(axis=direction, degrees=degree)).transformation_matrix
    trans[0:3, 3] = np.asarray(pos)
    pcd.transform(trans)
    return pcd


def __createArrow(config) -> o3d.geometry.TriangleMesh:
    scale = config.get('axisScale', 1 / 100)
    return o3d.geometry.TriangleMesh.create_arrow(
        cylinder_radius=scale * 0.8,
        cone_radius=scale * 1.5,
        cylinder_height=scale * 10,
        cone_height=scale * 4
    )


def __createXAxis(config) -> List[o3d.geometry.Geometry]:
    scale = config.get('axisScale', 1 / 100)
    color = [1, 0, 0]
    arrow = __createArrow(config)
    arrow.paint_uniform_color(color)
    R = o3d.geometry.get_rotation_matrix_from_xyz([0, np.pi / 2, 0])
    arrow = arrow.rotate(R, center=[0, 0, 0])

    result = [arrow]
    if config.get('axisLabelEnable', True):
        label = __text3D("X", config, pos=[scale * 14, -scale * 2, 0.0])
        label.paint_uniform_color(color)
        result.append(label)
    return result


def __createYAxis(config) -> List[o3d.geometry.Geometry]:
    scale = config.get('axisScale', 1 / 100)
    color = [0, 1, 0]
    arrow = __createArrow(config)
    arrow.paint_uniform_color(color)
    R = o3d.geometry.get_rotation_matrix_from_xyz([-np.pi / 2, 0, 0])
    arrow = arrow.rotate(R, center=[0, 0, 0])

    result = [arrow]
    if config.get('axisLabelEnable', True):
        label = __text3D("Y", config, pos=[-scale * 3, scale * 14, 0.0])
        label.paint_uniform_color(color)
        result.append(label)
    return result


def __createZAxis(config) -> List[o3d.geometry.Geometry]:
    scale = config.get('axisScale', 1 / 100)
    color = [0, 0, 1]
    arrow = __createArrow(config)
    arrow.paint_uniform_color(color)

    result = [arrow]
    if config.get('axisLabelEnable', True):
        label = __text3D("Z", config, pos=[-scale * 3, -scale * 2, scale * 15])
        label.paint_uniform_color(color)
        result.append(label)
    return result


def __createAxis(config) -> List[o3d.geometry.Geometry]:
    return __createXAxis(config) + __createYAxis(config) + __createZAxis(config)
