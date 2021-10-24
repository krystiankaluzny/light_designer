import open3d as o3d
import open3d.visualization as o3dv
import numpy as np
from typing import List, Tuple


def changeBackgroundToBlack(vis):
    opt = vis.get_render_option()
    opt.background_color = np.asarray([0, 0, 0])
    return False


def changeBackgroundToWhite(vis):
    opt = vis.get_render_option()
    opt.background_color = np.asarray([1, 1, 1])
    return False


def text3D(text, pos, direction=None, degree=0.0, density=10, font='/usr/share/fonts/truetype/freefont/FreeMono.ttf', font_size=12) -> o3d.geometry.PointCloud():
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


def createArrow(scale=(1 / 100)) -> o3d.geometry.TriangleMesh:
    return o3d.geometry.TriangleMesh.create_arrow(
        cylinder_radius=scale * 0.8,
        cone_radius=scale * 1.5,
        cylinder_height=scale * 10,
        cone_height=scale * 4
    )


def createXAxis(scale=(1 / 100)) -> List[o3d.geometry.Geometry]:
    color = [1, 0, 0]
    arrow = createArrow(scale)
    arrow.paint_uniform_color(color)
    R = o3d.geometry.get_rotation_matrix_from_xyz([0, np.pi / 2, 0])
    arrow = arrow.rotate(R, center=[0, 0, 0])

    label = text3D("X", pos=[scale * 14, -scale * 2, 0.0])
    label.paint_uniform_color(color)
    return [arrow, label]


def createYAxis(scale=(1 / 100)) -> List[o3d.geometry.Geometry]:
    color = [0, 1, 0]
    arrow = createArrow(scale)
    arrow.paint_uniform_color(color)
    R = o3d.geometry.get_rotation_matrix_from_xyz([-np.pi / 2, 0, 0])
    arrow = arrow.rotate(R, center=[0, 0, 0])

    label = text3D("Y", pos=[-scale * 3, scale * 14, 0.0])
    label.paint_uniform_color(color)
    return [arrow, label]


def createZAxis(scale=(1 / 100)) -> List[o3d.geometry.Geometry]:
    color = [0, 0, 1]
    arrow = createArrow(scale)
    arrow.paint_uniform_color(color)

    label = text3D("Z", pos=[-scale * 3, -scale * 2, scale * 15])
    label.paint_uniform_color(color)
    return [arrow, label]


def createAxis() -> List[o3d.geometry.Geometry]:
    return createXAxis() + createYAxis() + createZAxis()


def rotate_x(vis):
    vc: o3dv.ViewControl = vis.get_view_control()
    vc.rotate(30, 0, 0)
    return False


def visualize(pointClouds: List[o3d.geometry.Geometry]):
    vis = o3dv.VisualizerWithKeyCallback()
    vis.register_key_callback(ord("B"), changeBackgroundToBlack)
    vis.register_key_callback(ord("W"), changeBackgroundToWhite)
    vis.register_key_callback(ord("X"), rotate_x)
    vis.create_window("Test")

    for pcd in pointClouds:
        vis.add_geometry(pcd)

    for axis in createAxis():
        vis.add_geometry(axis)

    # vis.add_geometry(createZArrow())
    opt = vis.get_render_option()
    # opt.show_coordinate_frame = True
    # vc: o3dv.ViewControl = vis.get_view_control()
    # vc.rotate(90, 0, 90)

    vis.run()  # until user presses "q" to terminate
    vis.destroy_window()
    # o3d.visualization.draw_geometries_with_key_callbacks(pointClouds, key_to_callback)
