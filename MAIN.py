import formfactors, import_file, linear_equations, triangle_mesh, color_convertion, visibility
import numpy as np
import time


def calculate_scene(filename, samples=4):
    start_time = time.time()
    print("filename = ",'"'+filename+'"') #Print needed for storage
    scene, objects = import_file.import_file(filename)
    nb_triangles = len(scene)
    triangle_areas = [triangle_mesh.triangle_area_carth(triangle) for triangle in scene]
    print("nb_triangles = ",nb_triangles) #Print needed for storage
    print("samples = ",samples) #Print needed for storage
    # print("scene = ", scene.tolist()) #Print needed for storage
    kdtree = visibility.build_kdtree(objects, nb_triangles,65,20)
    # print(visibility.count_triangles(kdtree))
    radiosity_matrix_red = np.identity(nb_triangles)
    radiosity_matrix_green = np.identity(nb_triangles)
    radiosity_matrix_blue = np.identity(nb_triangles)
    emission_red = np.zeros(nb_triangles)
    emission_green = np.zeros(nb_triangles)
    emission_blue = np.zeros(nb_triangles)
    for i in range(nb_triangles):
        # start = time.time()
        print(i)
        emission_red[i] = scene[i][5][0]
        emission_green[i] = scene[i][5][1]
        emission_blue[i] = scene[i][5][2]
        rhoi_red = scene[i][4][0]
        rhoi_green = scene[i][4][1]
        rhoi_blue = scene[i][4][2]
        triangleI = np.array(scene[i][0:4])
        areaI = triangle_areas[i]
        # print(emission_red[i])
        for j in range(i + 1, nb_triangles):
            triangleJ = np.array(scene[j][0:4])
            formfJI = formfactors.uniform(triangleJ, triangleI, areaI, kdtree, samples)
            if formfJI == 0.0:
                radiosity_matrix_red[i][j] = 0.0
                radiosity_matrix_red[j][i] = 0.0
                radiosity_matrix_green[i][j] = 0.0
                radiosity_matrix_green[j][i] = 0.0
                radiosity_matrix_blue[i][j] = 0.0
                radiosity_matrix_blue[j][i] = 0.0
            else:
                areaJ = triangle_areas[j]
                rhoj_red = scene[j][4][0]
                rhoj_green = scene[j][4][1]
                rhoj_blue = scene[j][4][2]
                radiosity_matrix_red[i][j] = -rhoi_red * formfJI
                radiosity_matrix_red[j][i] = -rhoj_red * formfJI * areaJ / areaI
                radiosity_matrix_green[i][j] = -rhoi_green * formfJI
                radiosity_matrix_green[j][i] = -rhoj_green * formfJI * areaJ / areaI
                radiosity_matrix_blue[i][j] = -rhoi_blue * formfJI
                radiosity_matrix_blue[j][i] = -rhoj_blue * formfJI * areaJ / areaI
        # end = time.time()
        # print(end-start)
    power_red = linear_equations.gauss_seidel(radiosity_matrix_red, emission_red, max_it=80) + emission_red
    power_green = linear_equations.gauss_seidel(radiosity_matrix_green, emission_green, max_it=80) + emission_green
    power_blue = linear_equations.gauss_seidel(radiosity_matrix_blue, emission_blue, max_it=80) + emission_blue

    print("power_red = ",power_red.tolist()) #Print needed for storage
    print("power_green = ", power_green.tolist()) #Print needed for storage
    print("power_blue = ", power_blue.tolist()) #Print needed for storage
    print("calculation_time = ", (time.time() - start_time)) #Print needed for storage

calculate_scene("gekregen ruimte test", samples=5)
