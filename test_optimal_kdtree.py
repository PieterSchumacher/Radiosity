import import_file, visibility, time, random

results = {}
name = "gekregen ruimte 3.0"
scene_array, objects = import_file.import_file(name)
scene = [0 for i in range(len(scene_array))]
for i in range(len(scene_array)):
    scene[i] = scene_array[i][:4]
V = visibility.determine_max_coordinates(scene)
random_points = []
for i in range(100000):
    random_x = (V[0][1]-V[0][0]) * random.random() + V[0][0]
    random_y = (V[1][1]-V[1][0]) * random.random() + V[1][0]
    random_z = (V[2][1]-V[2][0]) * random.random() + V[2][0]
    random_points.append([random_x,random_y,random_z])
minimal_time_visibility = {"time": None, "max_triangles": None, "max_depth": None, "scene": name}
for max_triangles in range(2,10):
    for max_depth in range(5,20):
        start = time.time()
        kd_tree = visibility.build_kdtree(objects, len(scene), max_triangles, max_depth)
        end = time.time()
        time_tree = end - start
        count = visibility.count_triangles(kd_tree)
        #checking visibility of the 1000 pairs of random points
        start = time.time()
        for i in range(0,100000,2):
            visible = visibility.visible(kd_tree, random_points[i], random_points[i+1])
        end = time.time()
        time_visible = end - start
        if minimal_time_visibility["time"] == None or time_visible < minimal_time_visibility["time"]:
            minimal_time_visibility["time"] = time_visible
            minimal_time_visibility["max_triangles"] = max_triangles
            minimal_time_visibility["max_depth"] = max_depth
            minimal_time_visibility["count"] = count

        results[(max_triangles,max_depth)] = [time_tree, time_visible, time_tree+time_visible]

print("file = ",name)
print("results = ", results)
print("minimal = ", minimal_time_visibility)