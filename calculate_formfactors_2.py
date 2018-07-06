import numpy as np
import formfactors
import multiprocessing
import math
import triangle_mesh
import visibility
from formfactors import normal_opt, integrand


def worker(start, end, triangleI, areaI, scene, kdtree, samples, output):
    form_factors = np.zeros(end-start)
    for j in range(start, end):
        triangleJ = np.array(scene[j][0:4])
        form_factors[j-start] = formfactors.uniform(triangleJ, triangleI, areaI, kdtree, samples)
    output.send(form_factors)
    output.close()


def calculate_formfactors(triangleI, areaI, scene, kdtree, samples, outputs, nb_processes, intervals):
    jobs = []
    print(intervals)
    for k in range(nb_processes):
        p = multiprocessing.Process(target=worker,
                                    args=(intervals[k][0], intervals[k][1], triangleI, areaI, scene, kdtree,
                                          samples, outputs[k][1],))
        jobs.append(p)
    for p in jobs:
        p.start()
    for p in jobs:
        p.join()


def uniform(triangleJ, triangleI, areaI, kdtree, samples):
    """
    Uniforme monte-carlo integratie van de vormfactor
    samples zijn standaard = 4
    """
    centroidJ, centroidI = triangle_mesh.centroid(triangleJ), triangle_mesh.centroid(triangleI)
    if normal_opt(triangleJ,triangleI,centroidJ,centroidI):
        return 0.0
    if int(areaI) > samples:
        samples = int(areaI) + 1
    dist_crit = math.sqrt(areaI/(3.2*samples))
    angles = triangle_mesh.angle_second(triangleI, triangleJ, centroidI, centroidJ)
    centr_dist = triangle_mesh.distance(centroidJ,centroidI)
    som = 0.0
    formfactor = 0.0
    if visibility.visible(kdtree, centroidI, centroidJ):
        som += integrand(angles[0], angles[1], centr_dist)
    counter = 1.0
    while counter < samples:
        # print("point ", k)
        # print(triangleI)
        pointI = triangle_mesh.random_point2(triangleI)
        pointJ = triangle_mesh.random_point2(triangleJ)
        dist = triangle_mesh.distance(pointI,pointJ)
        if dist > dist_crit:
            # print(pointI,pointJ)
            visible = visibility.visible(kdtree, pointI, pointJ)
            # print(pointI,pointJ,visible)
            # print("visible:", visible)
            if visible:
                # print("checked visibility")
                angles = triangle_mesh.angle_second(triangleI, triangleJ, pointI, pointJ)
                som += integrand(angles[0], angles[1], dist)
            counter +=1.0
        else:
            samples += 1
            dist = centr_dist
            angles = triangle_mesh.angle_second(triangleI, triangleJ, pointI, pointJ)
            som += integrand(angles[0], angles[1], dist)
            counter +=1.0
    # print(som, samples, triangle_mesh.triangle_area_carth(triangleI))
    formfactor = som/float(counter)*areaI
    return formfactor


