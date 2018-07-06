import math
import triangle_mesh
import visibility
import import_file
import numpy as np
import time


def normal_opt(triangleJ, triangleI, centroidJ, centroidI):
    """
    Geeft True terug indien:
            1) normalen van 2 driehoeken gelijk zijn == kanten van driehoek beschijnen elkaar nooit
            2) de normalen hoeken maken van meer dan 90 graden en naar een andere richting dan naar de andere driehoek zijn gericht
    """
    normalI, normalJ = triangleI[3], triangleJ[3]
    if np.allclose(normalJ, normalI, atol=0.02):
        return True
    if not np.allclose(normalI,-normalJ,atol=0.01):
        Jbelicht = centroidJ - centroidI
        Ibelicht = centroidI- centroidJ
        if np.dot(Jbelicht,normalI) < 0.0 or np.dot(Ibelicht,normalJ) < 0.0:
            return True
    return False
        
        
def integrand(cosI,cosJ,r):
    """
    Integrand van de functie die moet worden geintegreerd
    """
    #print("cosI", cosI,"cosJ",cosJ,"r",r)
    return float(cosI*cosJ/(math.pi * r**2))


def uniform(triangleJ, triangleI, areaI, kdtree, samples=4):
    """
    Uniforme monte-carlo integratie van de vormfactor
    samples zijn standaard = 4
    """
    #print("calculating formfactor")
    centroidJ, centroidI = triangle_mesh.centroid(triangleJ), triangle_mesh.centroid(triangleI)
    if normal_opt(triangleJ,triangleI,centroidJ,centroidI):
        return 0.0
    if int(areaI) > samples:
        samples = int(areaI) + 1
    dist_crit = (areaI/(3.2*samples))**0.5
    angles = triangle_mesh.angle_second(triangleI, triangleJ, centroidI, centroidJ)
    centr_dist = triangle_mesh.distance(centroidJ,centroidI)
    som = 0.0
    formfactor = 0.0
    if visibility.visible(kdtree, centroidI, centroidJ):
        som += integrand(angles[0], angles[1], centr_dist)
    else:
        return 0.0
    counter = 1.0
    while counter < samples:
        # print("point ", k)
        # print(triangleI)
        pointI = triangle_mesh.random_point2(triangleI)
        pointJ = triangle_mesh.random_point2(triangleJ)
        dist = triangle_mesh.distance(pointI,pointJ)
        if dist > dist_crit:
            # print(pointI,pointJ)
            # visible = visibility.visible(kdtree, pointI, pointJ)
            # print(pointI,pointJ,visible)
            # print("visible:", visible)
            # if visible:
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


def uniform_cheat(triangleJ, triangleI, areaI, kdtree, samples=6):
    """
    Uniforme monte-carlo integratie van de vormfactor
    samples zijn standaard = 6
    Hoeken en visibility worden maar 1 keer berekend
    Uit tests blijkt dit toch niet zo precies :(
    """
    som = 0.0
    dist_crit = math.sqrt(areaI/(3.2*samples))
    p, q = triangle_mesh.centroid(triangleI), triangle_mesh.centroid(triangleJ)
    dist = triangle_mesh.distance(p,q)
    if dist <= dist_crit:
        return uniform(triangleJ, triangleI, kdtree, samples=6)
    angles = triangle_mesh.angle_second(triangleI, triangleJ, p, q)
    if not visibility.visible(kdtree, p,q):
        return 0.0
    som += integrand(angles[0], angles[1], triangle_mesh.distance(p,q))
    for k in range(samples-1):
        pointI = triangle_mesh.random_point2(triangleI)
        pointJ = triangle_mesh.random_point2(triangleJ)
        angles = triangle_mesh.angle_second(triangleI, triangleJ, pointI, pointJ)
        som += integrand(angles[0], angles[1], triangle_mesh.distance(pointI,pointJ))
    samples = float(samples)
    formfactor = som/samples*areaI
    return formfactor



def cheat_integration(triangleJ, triangleI, areaI, kdtree):
    """
    Voor als de driehoeken zeer klein zijn
    """

    p, q = triangle_mesh.centroid(triangleI), triangle_mesh.centroid(triangleJ)
    angles = triangle_mesh.angle_second(triangleI, triangleJ, p, q)
    # start = time.time()
    visible = visibility.visible(kdtree, p, q)

    if visible:
        return areaI*integrand(angles[0], angles[1], triangle_mesh.distance(p, q))
    return 0.0


def stratisfied(triangleJ, triangleI, areaI, kdtree, samples=1, depth=1):
    """
    Stratisfied_simple berekent de integraal van de vormfactoren.
    depth = het aantal keer dat de driehoek wordt opgedeeld in drie, het totaal aantal samples = samples*(9**depth)
    
    """
    if depth == 0:
        return uniform(triangleJ, triangleI, areaI, kdtree, samples)
    else:
        centroidI, centroidJ = triangle_mesh.centroid(triangleI), triangle_mesh.centroid(triangleJ)
        I0, I1, I2 = np.array(triangleI), np.array(triangleI), np.array(triangleI)
        J0, J1, J2 = np.array(triangleJ), np.array(triangleJ), np.array(triangleJ)
        I0[0], I1[1],I2[2] = centroidI, centroidI, centroidI
        J0[0], J1[1],J2[2] = centroidJ, centroidJ, centroidJ
        return (stratisfied(J0,I0,areaI/3.0,kdtree,samples,depth-1)+stratisfied(J0,I1,areaI/3.0,kdtree,samples,depth-1)+stratisfied(J0,I2,areaI/3.0,kdtree,samples,depth-1)+stratisfied(J1,I0,areaI/3.0,kdtree,samples,depth-1)+stratisfied(J1,I1,areaI/3.0,kdtree,samples,depth-1)+stratisfied(J1,I2,areaI/3.0,kdtree,samples,depth-1)+stratisfied(J2,I0,areaI/3.0,kdtree,samples,depth-1)+stratisfied(J2,I1,areaI/3.0,kdtree,samples,depth-1)+stratisfied(J2,I2,areaI/3.0,kdtree,samples,depth-1))/3.0


def split_triangles(triangleI, degree, triangles=[]):

    """
    Split_triangle verdeelt een driehoek in kleinere driehoekjes door nieuwe driehoeken te creeeren,
    gevormd door de middens van de originele zijden.
    PARAM:
    triangle == de originele driehoek die gesplitst wordt
    degree geeft de graad van splitsing aan.
        Bv. degree == 1 -> 3 driehoekjes
            degree == 2 -> 16 driehoekjes
    triangles is een lijst met alle opgeslagen driehoekjes
    """

    if degree == 0:
        triangles.append(triangleI)
        return triangles

    vertex0 = triangleI[0]
    vertex1 = triangleI[1]
    vertex2 = triangleI[2]

    mid0 = [(vertex0[0]+vertex1[0])/2,
            (vertex0[1]+vertex1[1])/2,
            (vertex0[2]+vertex1[2])/2]
    mid1 = [(vertex1[0]+vertex2[0])/2,
            (vertex1[1]+vertex2[1])/2,
            (vertex1[2]+vertex2[2])/2]
    mid2 = [(vertex2[0]+vertex0[0])/2,
            (vertex2[1]+vertex0[1])/2,
            (vertex2[2]+vertex0[2])/2]

    triangles_to_process = []
    triangles_to_process.append([[vertex0[0],vertex0[1],vertex0[2]],[mid0[0],mid0[1],mid0[2]],[mid2[0],mid2[1],mid2[2]]])
    triangles_to_process.append([[mid0[0],mid0[1],mid0[2]],[vertex1[0],vertex1[1],vertex1[2]],[mid1[0],mid1[1],mid1[2]]])
    triangles_to_process.append([[mid2[0],mid2[1],mid2[2]],[mid1[0],mid1[1],mid1[2]],[vertex2[0],vertex2[1],vertex2[2]]])
    triangles_to_process.append([[mid0[0],mid0[1],mid0[2]],[mid1[0],mid1[1],mid1[2]],[mid2[0],mid2[1],mid2[2]]])

    for triangle in triangles_to_process:
        split_triangles(triangle,triangles,degree-1)
    return triangles

# scene = import_file.import_file("cornellbox-test-2-lamp")
# triangles = [[[0 for i in range(3)] for i in range(3)] for i in range(len(scene))]
# for i in range(len(scene)):
#     for j in range(3):
#         for k in range(3):
#             triangles[i][j][k]=scene[i][j][k]
# kdtree = visibility.build_kdtree(scene)
# for i in range(0,len(scene)):
#     for j in range(1,i):
#         uniform(scene[i][0:3],scene[j][0:3],kdtree, samples=1)
