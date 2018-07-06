import numpy as np

def import_file(name):
    """
    Imports .obj and .mlt file
    :param name: name of the files (without extensions, normally the same) in a STRING
    :return: np array of all triangles
    (triangle = np array of 3 points (of 3 coordinates), the normal, the diffuse coefficient)
    """
    mtl = open('3Dscenes/'+name+'.mtl')
    list_mtl = mtl.readlines()
    dic_kd = {}
    dic_ke = {}
    for i in range(len(list_mtl)):
        if list_mtl[i][:6] == 'newmtl':
            if list_mtl[i+3][:2] == 'Kd':
                dic_kd[list_mtl[i][7:-1]] = list_mtl[i+3].split()[1:]
            else:
                dic_kd[list_mtl[i][7:-1]] = [0,0,0]
            if list_mtl[i+5][:2] == 'Ke':
                dic_ke[list_mtl[i][7:-1]] = list_mtl[i+5].split()[1:]
            else:
                dic_ke[list_mtl[i][7:-1]] = [0, 0, 0]
    obj = open('3Dscenes/'+name+'.obj')
    list_obj = obj.readlines()
    vertices = []
    faces = []
    normal = []
    objects = {}
    kd = np.zeros(3)
    ke = np.zeros(3)
    for line in list_obj:
        if line[:6] == 'usemtl':
            kd = dic_kd[line[7:-1]]
            ke = dic_ke[line[7:-1]]
        elif line[0] == 'o':
            key = line[2:-1]
            objects[key] = []
        elif line[:2] == 'v ':
            vertices.append(line.split()[1::])
        elif line[0] == 'f':
            faces.append(line.split()[1::]+[kd]+[ke])
            objects[key].append(line.split()[1::])
        elif line[:2] == 'vn':
            normal.append(line.split()[1::])
    for obj in objects.keys():
        for i in range(len(objects[obj])):
            for m in range(3):
                first_slash = objects[obj][i][m].index('/')
                last_slash = objects[obj][i][m].rfind('/')
                vertix_index = objects[obj][i][m][:first_slash]
                normal_index = objects[obj][i][m][last_slash + 1:]
                objects[obj][i][m] = np.zeros(3)
                objects[obj][i][m][0] = float(vertices[int(vertix_index) - 1][0])
                objects[obj][i][m][1] = float(vertices[int(vertix_index) - 1][2])
                objects[obj][i][m][2] = float(vertices[int(vertix_index) - 1][1])
            objects[obj][i].append([0 for i in range(3)])
            for k in range(3):
                objects[obj][i][3][k] = float(normal[int(normal_index)-1][k])
    nb_triangles = len(faces)
    scene = np.zeros((nb_triangles,6,3))
    for i in range(len(faces)):
        if len(faces[i]) != 5:
            print("ERROR: not triangle")
        for j in range(len(faces[0])-2):
            first_slash = faces[i][j].index('/')
            last_slash = faces[i][j].rfind('/')
            vertix_index = faces[i][j][:first_slash]
            normal_index = faces[i][j][last_slash+1:]
            scene[i][j][0] = float(vertices[int(vertix_index)-1][0])
            scene[i][j][1] = float(vertices[int(vertix_index)-1][1])
            scene[i][j][2] = float(vertices[int(vertix_index)-1][2])
        for k in range(3):
            scene[i][3][k] = normal[int(normal_index)-1][k]
            scene[i][4][k] = faces[i][3][k]
            scene[i][5][k] = faces[i][4][k]
        scene[i][3] = np.round(scene[i][3],1)
        scene[i][3] /= np.linalg.norm(scene[i][3])
    scene_dct = {}
    for k in range(len(scene)):
        scene_dct[k] = scene[k]
    return scene_dct, objects
