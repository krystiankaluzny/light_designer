import open3d as o3d
import open3d.visualization as o3dv
import numpy as np
from typing import List

class Visualizer(object):

    def __init__(self, vis: o3dv.VisualizerWithKeyCallback):
        self.vis = vis

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


def visualizerOf(geometries: List[o3d.geometry.Geometry], axis=True):
    vis = o3dv.VisualizerWithKeyCallback()
    vis.register_key_callback(ord("B"), __changeBackgroundToBlack)
    vis.register_key_callback(ord("W"), __changeBackgroundToWhite)
    vis.register_key_callback(ord("Q"), __quit)
    vis.create_window("Test")

    if axis:
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


def __text3D(text, pos, direction=None, degree=0.0, density=10, font='/usr/share/fonts/truetype/freefont/FreeMono.ttf', font_size=12) -> o3d.geometry.PointCloud():
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


def __createArrow(scale=(1 / 100)) -> o3d.geometry.TriangleMesh:
    return o3d.geometry.TriangleMesh.create_arrow(
        cylinder_radius=scale * 0.8,
        cone_radius=scale * 1.5,
        cylinder_height=scale * 10,
        cone_height=scale * 4
    )


def __createXAxis(scale=(1 / 100)) -> List[o3d.geometry.Geometry]:
    color = [1, 0, 0]
    arrow = __createArrow(scale)
    arrow.paint_uniform_color(color)
    R = o3d.geometry.get_rotation_matrix_from_xyz([0, np.pi / 2, 0])
    arrow = arrow.rotate(R, center=[0, 0, 0])

    label = __text3D("X", pos=[scale * 14, -scale * 2, 0.0])
    label.paint_uniform_color(color)
    return [arrow, label]


def __createYAxis(scale=(1 / 100)) -> List[o3d.geometry.Geometry]:
    color = [0, 1, 0]
    arrow = __createArrow(scale)
    arrow.paint_uniform_color(color)
    R = o3d.geometry.get_rotation_matrix_from_xyz([-np.pi / 2, 0, 0])
    arrow = arrow.rotate(R, center=[0, 0, 0])

    label = __text3D("Y", pos=[-scale * 3, scale * 14, 0.0])
    label.paint_uniform_color(color)
    return [arrow, label]


def __createZAxis(scale=(1 / 100)) -> List[o3d.geometry.Geometry]:
    color = [0, 0, 1]
    arrow = __createArrow(scale)
    arrow.paint_uniform_color(color)

    label = __text3D("Z", pos=[-scale * 3, -scale * 2, scale * 15])
    label.paint_uniform_color(color)
    return [arrow, label]


def __createAxis() -> List[o3d.geometry.Geometry]:
    return __createXAxis() + __createYAxis() + __createZAxis()
