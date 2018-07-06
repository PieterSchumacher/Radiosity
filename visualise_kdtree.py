import vtk, visibility, import_file
import numpy as np

scene, objects = import_file.import_file("cornell ext en r vlakken")
kdtree = visibility.build_kdtree(objects, len(scene))
polygons = []
def add_split_polygon(polygon, node):
    print(node.data)
    if not isinstance(node.data,float):
        print("is in leaf")
        return polygon
    else:
        V = node.bounding_box
        axis = V[3] % 3
        new_polygon = []
        if axis == 0:
            new_polygon.append([[node.data,V[1][0],V[2][0]],[node.data,V[1][1],V[2][0]],[node.data,V[1][0],V[2][1]],\
                               [node.data,V[1][1],V[2][1]]])
        elif axis == 1:
            new_polygon.append([[V[0][0],node.data,V[2][0]],[V[0][1],node.data,V[2][0]],[V[0][0],node.data,V[2][1]],\
                               [V[0][1],node.data,V[2][1]]])
        elif axis == 2:
            new_polygon.append([[V[0][0],V[1][0],node.data],[V[0][0],V[1][1],node.data],[V[0][0],V[1][0],node.data],\
                               [V[0][0],V[1][1],node.data]])
        add_split_polygon(polygon,node.left_child)
        add_split_polygon(polygon,node.right_child)

add_split_polygon(polygons,kdtree)
print(polygons)

vertices = []
for triangle in scene:
    vertices.append(triangle[:-2])
polygon_data = np.array(polygons)
# polygon_colors_data = [[255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255]]
triangle_data = np.array(vertices)
triangle_color_data = [[255, 255, 255] for i in range(len(vertices))]

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
