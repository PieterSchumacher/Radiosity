#adjust the first import to the file you want to visualise
import Gekregen_test as imported_file
import numpy as np
import vtk
import triangle_mesh
import color_convertion
import import_file_mp


scene, objects = import_file_mp.import_file("gekregen ruimte test")

triangle_areas = [triangle_mesh.triangle_area_carth(scene[k][0:3]) for k in range(len(scene))]
nb_triangles = len(scene)
power_red = imported_file.power_red
power_green = imported_file.power_green
power_blue = imported_file.power_blue

# Conversie naar watt/m²
for i in range(len(power_red)):
    power_red[i] /= (triangle_areas[i])
    power_green[i] /= (triangle_areas[i])
    power_blue[i] /= (triangle_areas[i])

# Conversie van vermogens naar kleuren met gamma correctie
rgb_values = color_convertion.convert_power_to_color(power_red, power_green, power_blue, nb_triangles)
rgb_red, rgb_green, rgb_blue = rgb_values[0], rgb_values[1], rgb_values[2]

colors = np.array([np.zeros(3) for k in range(nb_triangles)])
vertices = np.array([np.array([np.zeros(3) for k in range(3)]) for i in range(nb_triangles)])
for k in range(len(scene)):
    colors[k][0], colors[k][1], colors[k][2] = rgb_red[k], rgb_green[k], rgb_blue[k]
    vertices[k] = scene[k][0:3]


#print(colors)
# create a rendering window and renderer
ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)

# create a renderwindowinteractor
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

# create points
points = vtk.vtkPoints()
triangles = vtk.vtkCellArray()

# setup colors (setting the name to "Colors" is nice but not necessary)
Colors = vtk.vtkUnsignedCharArray()
Colors.SetNumberOfComponents(3)
Colors.SetName("Colors")

index = 0
for i in range(len(vertices)):
    points.InsertNextPoint(vertices[i][0])
    points.InsertNextPoint(vertices[i][1])
    points.InsertNextPoint(vertices[i][2])

    triangle = vtk.vtkTriangle()
    triangle.GetPointIds().SetId(0, index)
    triangle.GetPointIds().SetId(1, index + 1)
    triangle.GetPointIds().SetId(2, index + 2)
    triangles.InsertNextCell(triangle)
    Colors.InsertNextTuple3(colors[i][0], colors[i][1], colors[i][2])
    index += 3

# polydata object
trianglePolyData = vtk.vtkPolyData()
trianglePolyData.SetPoints(points)
trianglePolyData.SetPolys(triangles)

trianglePolyData.GetCellData().SetScalars(Colors)
trianglePolyData.Modified()
if vtk.VTK_MAJOR_VERSION <= 5:
    trianglePolyData.Update()

writer = vtk.vtkXMLPolyDataWriter()
writer.SetFileName("TriangleSolidColor.vtp")
if vtk.VTK_MAJOR_VERSION <= 5:
    writer.SetInput(trianglePolyData)
else:
    writer.SetInputData(trianglePolyData)
writer.Write()

# mapper
mapper = vtk.vtkPolyDataMapper()
if vtk.VTK_MAJOR_VERSION <= 5:
    mapper.SetInput(trianglePolyData)
else:
    mapper.SetInputData(trianglePolyData)

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
