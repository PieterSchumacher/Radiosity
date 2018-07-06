import numpy as np
import formfactors
from subdivide_loop import subdivide_loop
import multiprocessing


def worker(start, end, triangleI, areaI, scene, kdtree, samples, output, max_interval_length, step):
    # print("end - start: ", end-start)
    form_factors = np.zeros(end-start)
    for j in range(start, end):
        triangleJ = np.array(scene[j][0:4])
        form_factors[j-start] = formfactors.uniform(triangleJ, triangleI, areaI, kdtree, samples)
    result = output.get(block=True)
    for j in range(start, end):
        result[j-start] = form_factors[j-start]
    output.put(result)


def calculate_formfactors(start, end, triangleI, areaI, scene, kdtree, samples, output, nb_processes,
                          max_interval_length, step):
    intervals = subdivide_loop(start, end, max_interval_length, nb_processes)
    print("start")
    print(intervals)
    jobs = []
    for k in range(nb_processes):
        p = multiprocessing.Process(target=worker,
                                    args=(intervals[k][0], intervals[k][1], triangleI, areaI, scene, kdtree,
                                          samples, output, max_interval_length, step,))
        jobs.append(p)
    for p in jobs:
        p.start()
    for p in jobs:
        p.join()
    results = output.get()
    return results
