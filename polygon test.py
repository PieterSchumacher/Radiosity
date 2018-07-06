import vtk, visibility
import numpy as np

triangles = [[[1.25, 2.5, -0.9375], [0.9375, 2.5, -1.25], [0.9375, 2.5, -0.9375], [0.0, 1.0, 0.0]], [[0.0, 2.5, -0.9375], [-0.3125, 2.5, -1.25], [-0.3125, 2.5, -0.9375], [0.0, 1.0, 0.0]], [[0.0, 2.5, 0.3125], [-0.3125, 2.5, 0.0], [-0.3125, 2.5, 0.3125], [0.0, 1.0, 0.0]], [[1.25, 2.5, 0.3125], [0.9375, 2.5, 0.0], [0.9375, 2.5, 0.3125], [0.0, 1.0, 0.0]], [[0.625, 2.5, 0.3125], [0.3125, 2.5, 0.0], [0.3125, 2.5, 0.3125], [0.0, 1.0, 0.0]], [[0.625, 2.5, 0.9375], [0.3125, 2.5, 0.625], [0.3125, 2.5, 0.9375], [0.0, 1.0, 0.0]], [[1.25, 2.5, 0.9375], [0.9375, 2.5, 0.625], [0.9375, 2.5, 0.9375], [0.0, 1.0, 0.0]], [[-0.625, 2.5, 0.3125], [-0.9375, 2.5, 0.0], [-0.9375, 2.5, 0.3125], [0.0, 1.0, 0.0]], [[-0.625, 2.5, 0.9375], [-0.9375, 2.5, 0.625], [-0.9375, 2.5, 0.9375], [0.0, 1.0, 0.0]], [[0.0, 2.5, 0.9375], [-0.3125, 2.5, 0.625], [-0.3125, 2.5, 0.9375], [0.0, 1.0, 0.0]], [[-0.625, 2.5, -0.9375], [-0.9375, 2.5, -1.25], [-0.9375, 2.5, -0.9375], [0.0, 1.0, 0.0]], [[-0.625, 2.5, -0.3125], [-0.9375, 2.5, -0.625], [-0.9375, 2.5, -0.3125], [0.0, 1.0, 0.0]], [[0.0, 2.5, -0.3125], [-0.3125, 2.5, -0.625], [-0.3125, 2.5, -0.3125], [0.0, 1.0, 0.0]], [[0.625, 2.5, -0.9375], [0.3125, 2.5, -1.25], [0.3125, 2.5, -0.9375], [0.0, 1.0, 0.0]], [[0.625, 2.5, -0.3125], [0.3125, 2.5, -0.625], [0.3125, 2.5, -0.3125], [0.0, 1.0, 0.0]], [[1.25, 2.5, -0.3125], [0.9375, 2.5, -0.625], [0.9375, 2.5, -0.3125], [0.0, 1.0, 0.0]], [[0.9375, 2.5, -0.3125], [0.625, 2.5, -0.625], [0.625, 2.5, -0.3125], [0.0, 1.0, 0.0]], [[0.9375, 2.5, 0.0], [0.625, 2.5, -0.3125], [0.625, 2.5, 0.0], [0.0, 1.0, 0.0]], [[1.25, 2.5, 0.0], [0.9375, 2.5, -0.3125], [0.9375, 2.5, 0.0], [0.0, 1.0, 0.0]], [[0.3125, 2.5, -0.3125], [0.0, 2.5, -0.625], [0.0, 2.5, -0.3125], [0.0, 1.0, 0.0]], [[0.3125, 2.5, 0.0], [0.0, 2.5, -0.3125], [0.0, 2.5, 0.0], [0.0, 1.0, 0.0]], [[0.625, 2.5, 0.0], [0.3125, 2.5, -0.3125], [0.3125, 2.5, 0.0], [0.0, 1.0, 0.0]], [[0.3125, 2.5, -0.9375], [0.0, 2.5, -1.25], [0.0, 2.5, -0.9375], [0.0, 1.0, 0.0]], [[0.3125, 2.5, -0.625], [0.0, 2.5, -0.9375], [0.0, 2.5, -0.625], [0.0, 1.0, 0.0]], [[0.625, 2.5, -0.625], [0.3125, 2.5, -0.9375], [0.3125, 2.5, -0.625], [0.0, 1.0, 0.0]], [[-0.3125, 2.5, -0.3125], [-0.625, 2.5, -0.625], [-0.625, 2.5, -0.3125], [0.0, 1.0, 0.0]], [[-0.3125, 2.5, 0.0], [-0.625, 2.5, -0.3125], [-0.625, 2.5, 0.0], [0.0, 1.0, 0.0]], [[0.0, 2.5, 0.0], [-0.3125, 2.5, -0.3125], [-0.3125, 2.5, 0.0], [0.0, 1.0, 0.0]], [[-0.9375, 2.5, -0.3125], [-1.25, 2.5, -0.625], [-1.25, 2.5, -0.3125], [0.0, 1.0, 0.0]], [[-0.9375, 2.5, 0.0], [-1.25, 2.5, -0.3125], [-1.25, 2.5, 0.0], [0.0, 1.0, 0.0]], [[-0.625, 2.5, 0.0], [-0.9375, 2.5, -0.3125], [-0.9375, 2.5, 0.0], [0.0, 1.0, 0.0]], [[-0.9375, 2.5, -0.9375], [-1.25, 2.5, -1.25], [-1.25, 2.5, -0.9375], [0.0, 1.0, 0.0]], [[-0.9375, 2.5, -0.625], [-1.25, 2.5, -0.9375], [-1.25, 2.5, -0.625], [0.0, 1.0, 0.0]], [[-0.625, 2.5, -0.625], [-0.9375, 2.5, -0.9375], [-0.9375, 2.5, -0.625], [0.0, 1.0, 0.0]], [[-0.3125, 2.5, 0.9375], [-0.625, 2.5, 0.625], [-0.625, 2.5, 0.9375], [0.0, 1.0, 0.0]], [[-0.3125, 2.5, 1.25], [-0.625, 2.5, 0.9375], [-0.625, 2.5, 1.25], [0.0, 1.0, 0.0]], [[0.0, 2.5, 1.25], [-0.3125, 2.5, 0.9375], [-0.3125, 2.5, 1.25], [0.0, 1.0, 0.0]], [[-0.9375, 2.5, 0.9375], [-1.25, 2.5, 0.625], [-1.25, 2.5, 0.9375], [0.0, 1.0, 0.0]], [[-0.9375, 2.5, 1.25], [-1.25, 2.5, 0.9375], [-1.25, 2.5, 1.25], [0.0, 1.0, 0.0]], [[-0.625, 2.5, 1.25], [-0.9375, 2.5, 0.9375], [-0.9375, 2.5, 1.25], [0.0, 1.0, 0.0]], [[-0.9375, 2.5, 0.3125], [-1.25, 2.5, 0.0], [-1.25, 2.5, 0.3125], [0.0, 1.0, 0.0]], [[-0.9375, 2.5, 0.625], [-1.25, 2.5, 0.3125], [-1.25, 2.5, 0.625], [0.0, 1.0, 0.0]], [[-0.625, 2.5, 0.625], [-0.9375, 2.5, 0.3125], [-0.9375, 2.5, 0.625], [0.0, 1.0, 0.0]], [[0.9375, 2.5, 0.9375], [0.625, 2.5, 0.625], [0.625, 2.5, 0.9375], [0.0, 1.0, 0.0]], [[0.9375, 2.5, 1.25], [0.625, 2.5, 0.9375], [0.625, 2.5, 1.25], [0.0, 1.0, 0.0]], [[1.25, 2.5, 1.25], [0.9375, 2.5, 0.9375], [0.9375, 2.5, 1.25], [0.0, 1.0, 0.0]], [[0.3125, 2.5, 0.9375], [0.0, 2.5, 0.625], [0.0, 2.5, 0.9375], [0.0, 1.0, 0.0]], [[0.3125, 2.5, 1.25], [0.0, 2.5, 0.9375], [0.0, 2.5, 1.25], [0.0, 1.0, 0.0]], [[0.625, 2.5, 1.25], [0.3125, 2.5, 0.9375], [0.3125, 2.5, 1.25], [0.0, 1.0, 0.0]], [[0.3125, 2.5, 0.3125], [0.0, 2.5, 0.0], [0.0, 2.5, 0.3125], [0.0, 1.0, 0.0]], [[0.3125, 2.5, 0.625], [0.0, 2.5, 0.3125], [0.0, 2.5, 0.625], [0.0, 1.0, 0.0]], [[0.625, 2.5, 0.625], [0.3125, 2.5, 0.3125], [0.3125, 2.5, 0.625], [0.0, 1.0, 0.0]], [[0.9375, 2.5, 0.3125], [0.625, 2.5, 0.0], [0.625, 2.5, 0.3125], [0.0, 1.0, 0.0]], [[0.9375, 2.5, 0.625], [0.625, 2.5, 0.3125], [0.625, 2.5, 0.625], [0.0, 1.0, 0.0]], [[1.25, 2.5, 0.625], [0.9375, 2.5, 0.3125], [0.9375, 2.5, 0.625], [0.0, 1.0, 0.0]], [[-0.3125, 2.5, 0.3125], [-0.625, 2.5, 0.0], [-0.625, 2.5, 0.3125], [0.0, 1.0, 0.0]], [[-0.3125, 2.5, 0.625], [-0.625, 2.5, 0.3125], [-0.625, 2.5, 0.625], [0.0, 1.0, 0.0]], [[0.0, 2.5, 0.625], [-0.3125, 2.5, 0.3125], [-0.3125, 2.5, 0.625], [0.0, 1.0, 0.0]], [[-0.3125, 2.5, -0.9375], [-0.625, 2.5, -1.25], [-0.625, 2.5, -0.9375], [0.0, 1.0, 0.0]], [[-0.3125, 2.5, -0.625], [-0.625, 2.5, -0.9375], [-0.625, 2.5, -0.625], [0.0, 1.0, 0.0]], [[0.0, 2.5, -0.625], [-0.3125, 2.5, -0.9375], [-0.3125, 2.5, -0.625], [0.0, 1.0, 0.0]], [[0.9375, 2.5, -0.9375], [0.625, 2.5, -1.25], [0.625, 2.5, -0.9375], [0.0, 1.0, 0.0]], [[0.9375, 2.5, -0.625], [0.625, 2.5, -0.9375], [0.625, 2.5, -0.625], [0.0, 1.0, 0.0]], [[1.25, 2.5, -0.625], [0.9375, 2.5, -0.9375], [0.9375, 2.5, -0.625], [0.0, 1.0, 0.0]], [[1.25, 2.5, -0.9375], [1.25, 2.5, -1.25], [0.9375, 2.5, -1.25], [0.0, 1.0, 0.0]], [[0.0, 2.5, -0.9375], [0.0, 2.5, -1.25], [-0.3125, 2.5, -1.25], [0.0, 1.0, 0.0]], [[0.0, 2.5, 0.3125], [0.0, 2.5, 0.0], [-0.3125, 2.5, 0.0], [0.0, 1.0, 0.0]], [[1.25, 2.5, 0.3125], [1.25, 2.5, 0.0], [0.9375, 2.5, 0.0], [0.0, 1.0, 0.0]], [[0.625, 2.5, 0.3125], [0.625, 2.5, 0.0], [0.3125, 2.5, 0.0], [0.0, 1.0, 0.0]], [[0.625, 2.5, 0.9375], [0.625, 2.5, 0.625], [0.3125, 2.5, 0.625], [0.0, 1.0, 0.0]], [[1.25, 2.5, 0.9375], [1.25, 2.5, 0.625], [0.9375, 2.5, 0.625], [0.0, 1.0, 0.0]], [[-0.625, 2.5, 0.3125], [-0.625, 2.5, 0.0], [-0.9375, 2.5, 0.0], [0.0, 1.0, 0.0]], [[-0.625, 2.5, 0.9375], [-0.625, 2.5, 0.625], [-0.9375, 2.5, 0.625], [0.0, 1.0, 0.0]], [[0.0, 2.5, 0.9375], [0.0, 2.5, 0.625], [-0.3125, 2.5, 0.625], [0.0, 1.0, 0.0]], [[-0.625, 2.5, -0.9375], [-0.625, 2.5, -1.25], [-0.9375, 2.5, -1.25], [0.0, 1.0, 0.0]], [[-0.625, 2.5, -0.3125], [-0.625, 2.5, -0.625], [-0.9375, 2.5, -0.625], [0.0, 1.0, 0.0]], [[0.0, 2.5, -0.3125], [0.0, 2.5, -0.625], [-0.3125, 2.5, -0.625], [0.0, 1.0, 0.0]], [[0.625, 2.5, -0.9375], [0.625, 2.5, -1.25], [0.3125, 2.5, -1.25], [0.0, 1.0, 0.0]], [[0.625, 2.5, -0.3125], [0.625, 2.5, -0.625], [0.3125, 2.5, -0.625], [0.0, 1.0, 0.0]], [[1.25, 2.5, -0.3125], [1.25, 2.5, -0.625], [0.9375, 2.5, -0.625], [0.0, 1.0, 0.0]], [[0.9375, 2.5, -0.3125], [0.9375, 2.5, -0.625], [0.625, 2.5, -0.625], [0.0, 1.0, 0.0]], [[0.9375, 2.5, 0.0], [0.9375, 2.5, -0.3125], [0.625, 2.5, -0.3125], [0.0, 1.0, 0.0]], [[1.25, 2.5, 0.0], [1.25, 2.5, -0.3125], [0.9375, 2.5, -0.3125], [0.0, 1.0, 0.0]], [[0.3125, 2.5, -0.3125], [0.3125, 2.5, -0.625], [0.0, 2.5, -0.625], [0.0, 1.0, 0.0]], [[0.3125, 2.5, 0.0], [0.3125, 2.5, -0.3125], [0.0, 2.5, -0.3125], [0.0, 1.0, 0.0]], [[0.625, 2.5, 0.0], [0.625, 2.5, -0.3125], [0.3125, 2.5, -0.3125], [0.0, 1.0, 0.0]], [[0.3125, 2.5, -0.9375], [0.3125, 2.5, -1.25], [0.0, 2.5, -1.25], [0.0, 1.0, 0.0]], [[0.3125, 2.5, -0.625], [0.3125, 2.5, -0.9375], [0.0, 2.5, -0.9375], [0.0, 1.0, 0.0]], [[0.625, 2.5, -0.625], [0.625, 2.5, -0.9375], [0.3125, 2.5, -0.9375], [0.0, 1.0, 0.0]], [[-0.3125, 2.5, -0.3125], [-0.3125, 2.5, -0.625], [-0.625, 2.5, -0.625], [0.0, 1.0, 0.0]], [[-0.3125, 2.5, 0.0], [-0.3125, 2.5, -0.3125], [-0.625, 2.5, -0.3125], [0.0, 1.0, 0.0]], [[0.0, 2.5, 0.0], [0.0, 2.5, -0.3125], [-0.3125, 2.5, -0.3125], [0.0, 1.0, 0.0]], [[-0.9375, 2.5, -0.3125], [-0.9375, 2.5, -0.625], [-1.25, 2.5, -0.625], [0.0, 1.0, 0.0]], [[-0.9375, 2.5, 0.0], [-0.9375, 2.5, -0.3125], [-1.25, 2.5, -0.3125], [0.0, 1.0, 0.0]], [[-0.625, 2.5, 0.0], [-0.625, 2.5, -0.3125], [-0.9375, 2.5, -0.3125], [0.0, 1.0, 0.0]], [[-0.9375, 2.5, -0.9375], [-0.9375, 2.5, -1.25], [-1.25, 2.5, -1.25], [0.0, 1.0, 0.0]], [[-0.9375, 2.5, -0.625], [-0.9375, 2.5, -0.9375], [-1.25, 2.5, -0.9375], [0.0, 1.0, 0.0]], [[-0.625, 2.5, -0.625], [-0.625, 2.5, -0.9375], [-0.9375, 2.5, -0.9375], [0.0, 1.0, 0.0]], [[-0.3125, 2.5, 0.9375], [-0.3125, 2.5, 0.625], [-0.625, 2.5, 0.625], [0.0, 1.0, 0.0]], [[-0.3125, 2.5, 1.25], [-0.3125, 2.5, 0.9375], [-0.625, 2.5, 0.9375], [0.0, 1.0, 0.0]], [[0.0, 2.5, 1.25], [0.0, 2.5, 0.9375], [-0.3125, 2.5, 0.9375], [0.0, 1.0, 0.0]], [[-0.9375, 2.5, 0.9375], [-0.9375, 2.5, 0.625], [-1.25, 2.5, 0.625], [0.0, 1.0, 0.0]], [[-0.9375, 2.5, 1.25], [-0.9375, 2.5, 0.9375], [-1.25, 2.5, 0.9375], [0.0, 1.0, 0.0]], [[-0.625, 2.5, 1.25], [-0.625, 2.5, 0.9375], [-0.9375, 2.5, 0.9375], [0.0, 1.0, 0.0]], [[-0.9375, 2.5, 0.3125], [-0.9375, 2.5, 0.0], [-1.25, 2.5, 0.0], [0.0, 1.0, 0.0]], [[-0.9375, 2.5, 0.625], [-0.9375, 2.5, 0.3125], [-1.25, 2.5, 0.3125], [0.0, 1.0, 0.0]], [[-0.625, 2.5, 0.625], [-0.625, 2.5, 0.3125], [-0.9375, 2.5, 0.3125], [0.0, 1.0, 0.0]], [[0.9375, 2.5, 0.9375], [0.9375, 2.5, 0.625], [0.625, 2.5, 0.625], [0.0, 1.0, 0.0]], [[0.9375, 2.5, 1.25], [0.9375, 2.5, 0.9375], [0.625, 2.5, 0.9375], [0.0, 1.0, 0.0]], [[1.25, 2.5, 1.25], [1.25, 2.5, 0.9375], [0.9375, 2.5, 0.9375], [0.0, 1.0, 0.0]], [[0.3125, 2.5, 0.9375], [0.3125, 2.5, 0.625], [0.0, 2.5, 0.625], [0.0, 1.0, 0.0]], [[0.3125, 2.5, 1.25], [0.3125, 2.5, 0.9375], [0.0, 2.5, 0.9375], [0.0, 1.0, 0.0]], [[0.625, 2.5, 1.25], [0.625, 2.5, 0.9375], [0.3125, 2.5, 0.9375], [0.0, 1.0, 0.0]], [[0.3125, 2.5, 0.3125], [0.3125, 2.5, 0.0], [0.0, 2.5, 0.0], [0.0, 1.0, 0.0]], [[0.3125, 2.5, 0.625], [0.3125, 2.5, 0.3125], [0.0, 2.5, 0.3125], [0.0, 1.0, 0.0]], [[0.625, 2.5, 0.625], [0.625, 2.5, 0.3125], [0.3125, 2.5, 0.3125], [0.0, 1.0, 0.0]], [[0.9375, 2.5, 0.3125], [0.9375, 2.5, 0.0], [0.625, 2.5, 0.0], [0.0, 1.0, 0.0]], [[0.9375, 2.5, 0.625], [0.9375, 2.5, 0.3125], [0.625, 2.5, 0.3125], [0.0, 1.0, 0.0]], [[1.25, 2.5, 0.625], [1.25, 2.5, 0.3125], [0.9375, 2.5, 0.3125], [0.0, 1.0, 0.0]], [[-0.3125, 2.5, 0.3125], [-0.3125, 2.5, 0.0], [-0.625, 2.5, 0.0], [0.0, 1.0, 0.0]], [[-0.3125, 2.5, 0.625], [-0.3125, 2.5, 0.3125], [-0.625, 2.5, 0.3125], [0.0, 1.0, 0.0]], [[0.0, 2.5, 0.625], [0.0, 2.5, 0.3125], [-0.3125, 2.5, 0.3125], [0.0, 1.0, 0.0]], [[-0.3125, 2.5, -0.9375], [-0.3125, 2.5, -1.25], [-0.625, 2.5, -1.25], [0.0, 1.0, 0.0]], [[-0.3125, 2.5, -0.625], [-0.3125, 2.5, -0.9375], [-0.625, 2.5, -0.9375], [0.0, 1.0, 0.0]], [[0.0, 2.5, -0.625], [0.0, 2.5, -0.9375], [-0.3125, 2.5, -0.9375], [0.0, 1.0, 0.0]], [[0.9375, 2.5, -0.9375], [0.9375, 2.5, -1.25], [0.625, 2.5, -1.25], [0.0, 1.0, 0.0]], [[0.9375, 2.5, -0.625], [0.9375, 2.5, -0.9375], [0.625, 2.5, -0.9375], [0.0, 1.0, 0.0]], [[1.25, 2.5, -0.625], [1.25, 2.5, -0.9375], [0.9375, 2.5, -0.9375], [0.0, 1.0, 0.0]]]
polygon_data = visibility.join_triangles(triangles)[:-1]
# polygon_colors_data = [[255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255]]
triangle_data = [[[0, 0, 0], [-1, 0, -1], [0, 0, -1]]]
triangle_color_data = [[255, 255, 255], [255, 255, 255], [255, 255, 255]]

# create a rendering window and renderer
ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)

# create a renderwindowinteractor
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

# create points
triangle_points = vtk.vtkPoints()
polygon_points = vtk.vtkPoints()
triangles = vtk.vtkCellArray()
polygon = vtk.vtkPolygon()

# setup colors (setting the name to "Colors" is nice but not necessary)
triangle_colors = vtk.vtkUnsignedCharArray()
triangle_colors.SetNumberOfComponents(3)
# polygon_colors = vtk.vtkUnsignedCharArray()
# polygon_colors.SetNumberOfComponents(len(polygon_data))

index = 0
for i in range(len(triangle_data)):
    triangle_points.InsertNextPoint(triangle_data[i][0])
    triangle_points.InsertNextPoint(triangle_data[i][1])
    triangle_points.InsertNextPoint(triangle_data[i][2])

    triangle = vtk.vtkTriangle()
    triangle.GetPointIds().SetId(0, index)
    triangle.GetPointIds().SetId(1, index + 1)
    triangle.GetPointIds().SetId(2, index + 2)
    triangles.InsertNextCell(triangle)
    triangle_colors.InsertNextTuple3(triangle_color_data[i][0], triangle_color_data[i][1], triangle_color_data[i][2])
    index += 3

polygon.GetPointIds().SetNumberOfIds(len(polygon_data))
for j in range(len(polygon_data)):
    polygon_points.InsertNextPoint(polygon_data[j])
    polygon.GetPointIds().SetId(j, j)
    # polygon_colors.InsertNextTuple3(polygon_colors_data[j][0], polygon_colors_data[j][1], polygon_colors_data[j][2])

# CellArray object
polygons = vtk.vtkCellArray()
polygons.InsertNextCell(polygon)

# polydata object
trianglePolyData = vtk.vtkPolyData()
trianglePolyData.SetPoints(triangle_points)
trianglePolyData.SetPolys(triangles)
polygonPolyData = vtk.vtkPolyData()
polygonPolyData.SetPoints(polygon_points)
polygonPolyData.SetPolys(polygons)

trianglePolyData.GetCellData().SetScalars(triangle_colors)
trianglePolyData.Modified()
# polygonPolyData.GetCellData().SetScalars(polygon_colors)
# polygonPolyData.Modified()
if vtk.VTK_MAJOR_VERSION <= 5:
    trianglePolyData.Update()
    polygonPolyData.Update()

# mapper
mapper = vtk.vtkPolyDataMapper()
if vtk.VTK_MAJOR_VERSION <= 5:
    mapper.SetInput(trianglePolyData, polygonPolyData)
else:
    mapper.SetInputData(trianglePolyData)
    mapper.SetInputData(polygonPolyData)

# actor
actor = vtk.vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().LightingOff()

# assign actor to the renderer
ren.AddActor(actor)

# enable user interface interactor
iren.Initialize()
renWin.Render()
iren.Start()
