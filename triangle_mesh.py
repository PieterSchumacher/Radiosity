import numpy as np
import random
import time


def barycentric_coordinates(p, q):

    """
    Berekent de barycentrische coordinaten van een punt q in een gegeven driehoek met hoekpunten (p0,p1,p2)
    """

    p0, p1, p2 = p[0], p[1], p[2]
    n = np.cross([p1[0]-p0[0],p1[1]-p0[1],p1[2]-p0[2]],[p2[0]-p0[0],p2[1]-p0[1],p2[2]-p0[2]])
    na = np.cross([p2[0]-p1[0],p2[1]-p1[1],p2[2]-p1[2]], [q[0] - p1[0], q[1] - p1[1], q[2] - p1[2]])
    nb = np.cross([p0[0]-p2[0],p0[1]-p2[1],p0[2]-p2[2]], [q[0] - p2[0], q[1] - p2[1], q[2] - p2[2]])
    nc = np.cross([p1[0]-p0[0],p1[1]-p0[1],p1[2]-p0[2]], [q[0] - p0[0], q[1] - p0[1], q[2] - p0[2]])

    alfa = np.vdot(n,na)/(np.linalg.norm(n))**2
    beta = np.vdot(n,nb)/(np.linalg.norm(n))**2
    gamma = np.vdot(n,nc)/(np.linalg.norm(n))**2

    return alfa,beta,gamma


def centroid(p):
    """
    Berekent zwaartepunt van een driehoek p 
    :return: in cartesische coordinaten
    """
    return (p[0] + p[1] + p[2])/3.0
    

def centroid_bary(p):

    """
    Berekent het zwaartepunt van een gegeven driehoek met hoekpunten (p0,p1,p2)
    Zwaartepunt heeft als barycentrische coordinaten (1/3,1/3,1/3)
    Return in cartesische coordinaten
    """

    p0, p1, p2 = p[0], p[1], p[2]
    p = [0,0,0]
    beta = 1/3
    gamma = 1/3

    p[0] = (p1[0] - p0[0]) * beta + (p2[0] - p0[0]) * gamma + p0[0]
    p[1] = (p1[1] - p0[1]) * beta + (p2[1] - p0[1]) * gamma + p0[1]
    p[2] = (p1[2] - p0[2]) * beta + (p2[2] - p0[2]) * gamma + p0[2]

    return np.array(p)


def random_point(p):

    """
    Berekent een willekeurig punt binnen de gegeven driehoek met hoekpunten (p0,p1,p2)
    Punt wordt teruggegeven door numpy.array in cartesische coordinaten.
    """
    p0, p1, p2 = p[0], p[1], p[2]
    p  = [0,0,0]
    beta = random.uniform(0,1)
    gamma = random.uniform(0,1)
    if beta + gamma > 1.0:
        beta = 1.0-beta
        gamma = 1.0-gamma
    
    p[0] = (p1[0] - p0[0]) * beta + (p2[0] - p0[0]) * gamma + p0[0]
    p[1] = (p1[1] - p0[1]) * beta + (p2[1] - p0[1]) * gamma + p0[1]
    p[2] = (p1[2] - p0[2]) * beta + (p2[2] - p0[2]) * gamma + p0[2]

    return np.array(p)


def random_point2(p):
    """
    Berekent een random punt in de triangle met hoekpunten (p0,p1,p2) zonder omzetting
    naar barycentrische coordinaten.
    type(input) = type(output) = np.ndarray
    Methode overgenomen uit:
    Robert Osada, Thomas Funkhouser, Bernard Chazelle, and David Dobkin. 2002. Shape distributions. ACM Trans. Graph. 21, 4 (October 2002), 807-832. DOI=http://dx.doi.org/10.1145/571647.571648
    """
    r1, r2 = random.uniform(0,1), random.uniform(0,1)
    return (1-(r1**0.5))*p[0] + (r1**0.5)*(1-r2)*p[1] + (r1**0.5)*r2*p[2]


def triangle_area(p):
    """
    Berekent de oppervlakte van een gegeven driehoek a.d.h.v. barycentrische coordinaten.
    De oppervlakte is gelijk aan alfa+beta+gamma
    """

    p0, p1, p2 = p[0], p[1], p[2]
    normal = np.cross([p1[0]-p0[0],p1[1]-p0[1],p1[2]-p0[2]],[p2[0]-p0[0],p2[1]-p0[1],p2[2]-p0[2]])
    return float((1/2)*np.linalg.norm(normal))

def triangle_area_carth(p):
    "Berekent oppervlakte in adhv cathesische coodrinaten."
    return np.linalg.norm(np.cross(p[1]-p[0],p[2]-p[0]))/2.0


def distance(p, q):
    """
    Returns the distance between 2 3D points
    """
    #print("points ", p, q)
    #print("distance", np.linalg.norm(p-q))
    return np.linalg.norm(p-q)


def angle_second(p,q, pointI, pointJ):
    normal_p = p[3]
    normal_q = q[3]

    dire = pointJ - pointI
    cosI =  np.dot(normal_p, dire/np.linalg.norm(dire))
    cosJ =  np.dot(normal_q, dire/np.linalg.norm(dire))
    return cosI, -cosJ


def angle(p,q):

    """
    Berekent de cosinus van de hoek tussen de twee zwaartepunten (centroid) van twee driehoeken
    met hoekpunten (p0,p1,p2) en hoekpunten (q0,q1,q2)
    """

    p0, p1, p2 = p[0], p[1], p[2]
    q0, q1, q2 = q[0], q[1], q[2]
    normal_p = np.cross([p1[0] - p0[0], p1[1] - p0[1], p1[2] - p0[2]], [p2[0] - p0[0], p2[1] - p0[1], p2[2] - p0[2]])
    normal_q = np.cross([q1[0] - q0[0], q1[1] - q0[1], q1[2] - q0[2]], [q2[0] - q0[0], q2[1] - q0[1], q2[2] - q0[2]])
    centroid_p = centroid(p)
    centroid_q = centroid(q)
    vector_pq = [centroid_p[0]-centroid_q[0],centroid_p[1]-centroid_q[1],centroid_p[2]-centroid_q[2]]
    cos_p = abs(np.dot(normal_p,vector_pq)/(np.linalg.norm(normal_p)*np.linalg.norm(vector_pq)))
    cos_q = abs(np.dot(normal_q,vector_pq)/(np.linalg.norm(normal_q)*np.linalg.norm(vector_pq)))

    return cos_p,cos_q
