import formfactors, import_file_mp, linear_equations, triangle_mesh, color_convertion, visibility
import numpy as np
import time
import multiprocessing
from calculate_formfactors_2 import uniform


if __name__ == "__main__":
    def calculate_scene(filename, samples=4, start=None, end=None):
        print("filename = ",'"'+filename+'"') #Print needed for storage
        scene, objects = import_file_mp.import_file(filename)
        nb_triangles = len(scene)
        print("nb_triangles = ",nb_triangles) #Print needed for storage
        print("samples = ",samples) #Print needed for storage
        # print("scene = ", scene) #Print needed for storage
        triangle_areas = [triangle_mesh.triangle_area_carth(scene[k]) for k in range(len(scene))]
        kdtree = visibility.build_kdtree(objects, nb_triangles, 65, 20)
        # print(visibility.count_triangles(kdtree))
        radiosity_matrix_red = np.identity(nb_triangles)
        radiosity_matrix_green = np.identity(nb_triangles)
        radiosity_matrix_blue = np.identity(nb_triangles)
        emission_red = np.zeros(nb_triangles)
        emission_green = np.zeros(nb_triangles)
        emission_blue = np.zeros(nb_triangles)
        total_time = 0
        if start is None:
            start = 0
        if end is None:
            end = nb_triangles
        for i in range(start, end):
            start_time = time.time()
            print(i)
            emission_red[i] = scene[i][5][0]
            emission_green[i] = scene[i][5][1]
            emission_blue[i] = scene[i][5][2]
            rhoi_red = scene[i][4][0]
            rhoi_green = scene[i][4][1]
            rhoi_blue = scene[i][4][2]
            triangleI = np.array(scene[i][0:4])
            areaI = triangle_areas[i]
            pool = multiprocessing.Pool()
            triangles = []
            for j in range(i + 1, nb_triangles):
                triangles.append((np.array(scene[j][0:4]), triangleI, areaI, kdtree, samples))
            results = pool.starmap_async(uniform, triangles)
            pool.close()
            pool.join()
            form_factors = np.array(results.get())
            for j in range(i + 1, nb_triangles):
                if form_factors[j-(i+1)] == 0.0:
                    radiosity_matrix_red[i][j] = 0.0
                    radiosity_matrix_red[j][i] = 0.0
                    radiosity_matrix_green[i][j] = 0.0
                    radiosity_matrix_green[j][i] = 0.0
                    radiosity_matrix_blue[i][j] = 0.0
                    radiosity_matrix_blue[j][i] = 0.0
                else:
                    rhoj_red = scene[j][4][0]
                    rhoj_green = scene[j][4][1]
                    rhoj_blue = scene[j][4][2]
                    areaJ = triangle_areas[j]
                    radiosity_matrix_red[i][j] = -rhoi_red * form_factors[j-(i+1)]
                    radiosity_matrix_red[j][i] = -rhoj_red * form_factors[j-(i+1)] * areaJ / areaI
                    radiosity_matrix_green[i][j] = -rhoi_green * form_factors[j-(i+1)]
                    radiosity_matrix_green[j][i] = -rhoj_green * form_factors[j-(i+1)] * areaJ / areaI
                    radiosity_matrix_blue[i][j] = -rhoi_blue * form_factors[j-(i+1)]
                    radiosity_matrix_blue[j][i] = -rhoj_blue * form_factors[j-(i+1)] * areaJ / areaI

            total_time += time.time() - start_time
            print(total_time/(i+1))

        # Make a list of all triangles
        triangles = [(tuple(scene[i][0]), tuple(scene[i][1]), tuple(scene[i][2])) for i in range(len(scene))]
        # Make a new dict
        for key in objects.keys():
            for j in range(len(objects[key])):
                for k in range(len(objects[key][j])):
                    objects[key][j][k] = tuple(objects[key][j][k])
        # Iterate over emission values and, if ke != 0, divide by the amount of triangles in that plane
        for j in range(len(emission_red)):
            if emission_red[j] != 0 or emission_green[j] != 0 or emission_blue[j] != 0:
                for key in objects.keys():
                    for triangle in objects[key]:
                        if tuple(triangle[0:3]) == triangles[j]:
                            emission_red /= len(objects[key])
                            emission_green /= len(objects[key])
                            emission_blue /= len(objects[key])

        # Gauss Seidel met multiprocessing
        gauss_seidel_arguments = [(radiosity_matrix_red, emission_red, 80),
                                  (radiosity_matrix_green, emission_green, 80),
                                  (radiosity_matrix_blue, emission_blue, 80)]
        pool = multiprocessing.Pool()
        results = pool.starmap_async(linear_equations.gauss_seidel, gauss_seidel_arguments)
        pool.close()
        pool.join()
        results = np.array(results.get())
        power_red = results[0] + emission_red
        power_green = results[1] + emission_green
        power_blue = results[2] + emission_blue

        # Conversie naar watt/m²
        for i in range(len(power_red)):
            power_red[i] /= triangle_areas[i]
            power_green[i] /= triangle_areas[i]
            power_blue[i] /= triangle_areas[i]

        # Print powers
        print("power_red = ", power_red.tolist())
        print("power_green = ", power_green.tolist())
        print("power_blue = ", power_blue.tolist())

        # Conversie van vermogendichtheden naar kleuren met gamma correctie
        rgb_values = color_convertion.convert_power_to_color(power_red, power_green, power_blue, nb_triangles)
        rgb_red, rgb_green, rgb_blue = rgb_values[0], rgb_values[1], rgb_values[2]

        print("rgb_red = ", rgb_red.tolist())
        print("rgb_green = ", rgb_green.tolist())
        print("rgb_blue = ", rgb_blue.tolist())


    calculate_scene('gekregen ruimte heel fijn', samples=3)
