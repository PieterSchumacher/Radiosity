import import_file_mp, linear_equations, triangle_mesh, color_convertion, visibility, vtk
import numpy as np
import time
import multiprocessing

# Hier moet nog een import komen van alle uitgerekende data
data = np.load("matrices_test_0.npz")
radiosity_matrix_red = data['a']
radiosity_matrix_green = data['b']
radiosity_matrix_blue = data['c']

# Import emissions
scene, objects = import_file_mp("cba ruimte 2.0")
nb_triangles = len(scene)
emission_red = np.zeros(nb_triangles)
emission_green = np.zeros(nb_triangles)
emission_blue = np.zeros(nb_triangles)
for i in range(len(scene)):
    emission_red[i] = scene[i][5][0]
    emission_green[i] = scene[i][5][1]
    emission_blue[i] = scene[i][5][2]
triangle_areas = [triangle_mesh.triangle_area_carth(scene[k]) for k in range(len(scene))]

# Gauss Seidel met multiprocessing
gauss_seidel_arguments = [(radiosity_matrix_red, emission_red, 80),
                          (radiosity_matrix_green, emission_green, 80),
                          (radiosity_matrix_blue, emission_blue, 80)]
pool = multiprocessing.Pool()
results = pool.starmap_async(linear_equations.gauss_seidel, gauss_seidel_arguments)
pool.close()
pool.join()
power_red = results[0] + emission_red
power_green = results[1] + emission_green
power_blue = results[2] + emission_blue
for i in len(power_red):
    power_red[i] /= triangle_areas[i]
    power_green[i] /= triangle_areas[i]
    power_blue[i] /= triangle_areas[i]


# Print powers
print("power_red = ", power_red.tolist())
print("power_green = ", power_green.tolist())
print("power_blue = ", power_blue.tolist())

# Conversie naar watt/m²


# Conversie van vermogens naar kleuren met gamma correctie
rgb_values = color_convertion.convert_power_to_color(power_red, power_green, power_blue, nb_triangles)
rgb_red, rgb_green, rgb_blue = rgb_values[0], rgb_values[1], rgb_values[2]

print("rgb_red = ", rgb_red.tolist())
print("rgb_green = ", rgb_green.tolist())
print("rgb_blue = ", rgb_blue.tolist())

