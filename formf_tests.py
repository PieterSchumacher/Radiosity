import numpy as np
import triangle_mesh
import formfactors
import matplotlib.pyplot as plt
import math
import time


def uniform_test(triangleJ, triangleI, samples=4):
    """
    Uniforme monte-carlo integratie van de vormfactor
    samples zijn standaard = 4
    """
    #print("calculating formfactor")
    deler = samples
    som = 0.0
    for k in range(samples):
        # print("point ", k)
        # print(triangleI)
        pointI = triangle_mesh.random_point(triangleI)
        pointJ = triangle_mesh.random_point(triangleJ)
        # print(pointI,pointJ)
        dist = triangle_mesh.distance(pointI,pointJ)
        if dist >= 0.2:
            angles = triangle_mesh.angle_second(triangleI, triangleJ, pointI, pointJ)
            som += formfactors.integrand(np.clip(angles[0],0,1), np.clip(angles[1],0,1), dist)
        else:
            deler -=1
    # print(som, samples, triangle_mesh.triangle_area_carth(triangleI))
    deler = float(deler)
    area = triangle_mesh.triangle_area_carth(triangleI)
    formfactor = som/deler*area
    return formfactor


def uniform_test2(triangleJ, triangleI, areaI, samples=4):
    """
    Uniforme monte-carlo integratie van de vormfactor
    samples zijn standaard = 4
    """
    if int(areaI) > samples:
        samples = int(areaI) + 1
    stopcrit = samples + 10
    dist_crit = math.sqrt(areaI/(3.2*samples))
    centroidJ, centroidI = triangle_mesh.centroid(triangleJ), triangle_mesh.centroid(triangleI)
    angles = triangle_mesh.angle_second(triangleI, triangleJ, centroidI, centroidJ)
    centr_dist = triangle_mesh.distance(centroidJ,centroidI)
    som = 0.0
    formfactor = 0.0
    som += formfactors.integrand(angles[0], angles[1], centr_dist)
    counter = 1.0
    while counter < samples and stopcrit != 0:
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
            if True:
                # print("checked visibility")
                angles = triangle_mesh.angle_second(triangleI, triangleJ, pointI, pointJ)
                som += formfactors.integrand(angles[0], angles[1], dist)
            counter +=1.0
        else:
            samples += 1
            dist = centr_dist
            angles = triangle_mesh.angle_second(triangleI, triangleJ, pointI, pointJ)
            som += formfactors.integrand(angles[0], angles[1], dist)
            counter +=1.0

        stopcrit -= 1
            
    # print(som, samples, triangle_mesh.triangle_area_carth(triangleI))
    formfactor = som/float(counter)*areaI
    return formfactor


def uniform_cheat(triangleJ, triangleI, samples=6):
    """
    Uniforme monte-carlo integratie van de vormfactor
    samples zijn standaard = 6
    Hoeken en visibility worden maar 1 keer berekend
    """
    som = 0.0
    p, q = triangle_mesh.centroid(triangleI), triangle_mesh.centroid(triangleJ)
    angles = triangle_mesh.angle_second(triangleI, triangleJ, p, q)
    som += formfactors.integrand(angles[0], angles[1], triangle_mesh.distance(p,q))
    for k in range(samples-1):
        pointI = triangle_mesh.random_point(triangleI)
        pointJ = triangle_mesh.random_point(triangleJ)
        som += formfactors.integrand(angles[0], angles[1], triangle_mesh.distance(pointI,pointJ))
    samples = float(samples)
    area = triangle_mesh.triangle_area_carth(triangleI)
    formfactor = som/samples*area
    return formfactor


def stratisfied(triangleJ, triangleI, areaI, samples=1, depth=1):
    """
    Stratisfied_simple berekent de integraal van de vormfactoren.
    depth = het aantal keer dat de driehoek wordt opgedeeld in drie, het totaal aantal samples = samples*(3**depth)
    """
    if depth == 0:
        return uniform_test2(triangleJ, triangleI, areaI, samples)
    else:
        centroidI, centroidJ = triangle_mesh.centroid(triangleI), triangle_mesh.centroid(triangleJ)
        I0, I1, I2 = np.array(triangleI), np.array(triangleI), np.array(triangleI)
        J0, J1, J2 = np.array(triangleJ), np.array(triangleJ), np.array(triangleJ)
        I0[0], I1[1],I2[2] = centroidI, centroidI, centroidI
        J0[0], J1[1],J2[2] = centroidJ, centroidJ, centroidJ
        return (stratisfied(J0,I0,areaI,samples,depth-1)+stratisfied(J0,I1,areaI,samples,depth-1)+stratisfied(J0,I2,areaI,samples,depth-1)+stratisfied(J1,I0,areaI,samples,depth-1)+stratisfied(J1,I1,areaI,samples,depth-1)+stratisfied(J1,I2,areaI,samples,depth-1)+stratisfied(J2,I0,areaI,samples,depth-1)+stratisfied(J2,I1,areaI,samples,depth-1)+stratisfied(J2,I2,areaI,samples,depth-1))/3.0
    

"""
Test case 1:
    Twee driehoeken die rechte hoek met elkaar maken en 2 punten gemeensch hebben
"""
triangle1 = np.array([[0.,0.,0.],[0.,1.,1.],[0.,1.,0.],[1.,0.,0.]])
triangle2 = np.array([[0.,0.,0.],[0.,1.,0.],[1.,1.,0.],[0.,0.,1.]])
ref_value1 = .2
area1 = triangle_mesh.triangle_area_carth(triangle1)
print(area1)

triangleA = np.array([[0.,0.,0.],[0.,2.,2.],[0.,2.,0.],[1.,0.,0.]])
triangleB = np.array([[0.,0.,0.],[0.,2.,0.],[1.,2.,0.],[0.,0.,1.]])
ref_value2 = .3
areaA = triangle_mesh.triangle_area_carth(triangleA)
print(areaA)

triangleC = np.array([[0.,0.,0.],[0.,1.,10.],[0.,1.,0.],[1.,0.,0.]])
triangleD = np.array([[0.,0.,0.],[0.,1.,0.],[3.,1.,0.],[0.,0.,1.]])
ref_value3 = .5/3.02
areaC = triangle_mesh.triangle_area_carth(triangleC)


# som1 =0
# som2 =0
# som3 =0
# for k in range(50):
#     tmp1 = uniform_test2(triangle2,triangle1,area1,samples=60)
#     tmp2 = uniform_test2(triangleB,triangleA,areaA,samples=60)
#     tmp3 = uniform_test2(triangleC,triangleD,areaC,samples=60)
#     som1 += tmp1
#     som2 += tmp2
#     som3 += tmp3
#     # som2 += ref_value2
# som1 /= float(50)
# som2 /= float(50)
# som3 /= float(50)
# # som2 /= float(50)
# print(ref_value1,som1,ref_value2,som2,ref_value3,som3,sep="\n")
# 
# foutenlijst1 = []
# foutenlijst2 = []
# foutenlijst3 = []


"""
Test case2:
    Twee even grote driehoeken die evenwijdig aan elkaar zijn
"""
triangle3 = np.array([[0.,0.,0.],[2.,0.,0.],[0.,0.,2.],[0.,-4.,0.]])
triangle4 = np.array([[0.,4.,0.],[2.,4.,0.],[0.,4.,2.],[0.,-4.,0.]])
ref_value2 = .0359


# print(stratisfied(triangle1,triangle2,2,0))
# print(stratisfied(triangle1,triangle2,2,1))
# print(stratisfied(triangle1,triangle2,2,2))
# print(stratisfied(triangle3,triangle4,2,0))
# print(stratisfied(triangle3,triangle4,2,1))
# print(stratisfied(triangle3,triangle4,2,2))


# foutenlijst2 = []
# foutenlijst3 = []
# for k in range(1,31):
#     temp1, temp2, temp3 = 0.0, 0.0, 0.0
#     for j in range(200):
#         temp2 += (abs(ref_value1 - uniform_test2(triangle2,triangle1,area1,k)))
#         # temp3 += (abs(ref_value1 - uniform_test(triangle3,triangle4,k)))
#     foutenlijst2.append(temp2/200.0)
#     # foutenlijst3.append(temp3/20.0)


# t = list(range(1,31))
# 
# plt.figure(1)
# # plt.subplot(211)
# plt.title('Absolute fout voor testcase 1')
# plt.plot(t, foutenlijst2, 'ko',markersize=3)
# plt.xlabel('Aantal samples per formfactor')
# plt.ylabel('Absolute fout')
# # plt.subplot(212)
# # plt.plot(t, foutenlijst3, 'ko',markersize=5)
# # plt.xlabel('Aantal samples per formfactor')
# # plt.ylabel('Absolute fout')
# plt.show()

tijdslijst_uniform = []
for k in range(1,61):
    start = time.time()
    for j in range(500):
        uniform_test2(triangleD, triangleC, areaC, k)
    tijdslijst_uniform.append(time.time()-start)
t1 = list(range(1,61))

tijdslijst_stratisfied1 = []
for k in range(1,21):
    start = time.time()
    for j in range(500):
        stratisfied(triangleD, triangleC, areaC, k, 1)
    tijdslijst_stratisfied1.append(time.time()-start)
t2 = [3*j for j in range(1,21)]

tijdslijst_stratisfied2 = []
for k in range(1,7):
    start = time.time()
    for j in range(500):
        stratisfied(triangleD, triangleC, areaC, k, 2)
    tijdslijst_stratisfied2.append(time.time()-start)
t3 = [9*j for j in range(1,7)]

plt.plot(t1, tijdslijst_uniform,'ro', t2, tijdslijst_stratisfied1,'ko', t3, tijdslijst_stratisfied2,'bo',markersize=3)
plt.title('Snelheid van uniforme (rood) en gestratificeerde (met zwarte diepte 1 en blauw diepte 2) implementatie')
plt.xlabel('Aantal samples per vormfactor')
plt.ylabel('Tijd om vormfactor 500 keer uit te rekenen in seconden')
plt.show()
