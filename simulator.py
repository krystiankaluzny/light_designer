import open3d as o3d
import numpy as np
import visualizer as v

cone = o3d.geometry.TriangleMesh.create_cone()
arrow = o3d.geometry.TriangleMesh.create_arrow()
v.visualize([cone, arrow])
