import numpy as np
import copy as copy
from import_file import *
import time

class Node:
    def __init__(self, data, V, left_child = None, right_child = None):
        self.data = data
        self.left_child = left_child
        self.right_child = right_child
        self.bounding_box = V

    def add_child(self, left_child, right_child, V):
        self.left_child = left_child
        self.right_child = right_child

class Leaf:
    def __init__(self, data):
        self.data = data


def determine_max_coordinates(T):
    all_x_coord = []
    all_y_coord = []
    all_z_coord = []
    for triangle in T:
        for i in range(len(triangle) - 1):
            all_x_coord.append(triangle[i][0])
            all_y_coord.append(triangle[i][1])
            all_z_coord.append(triangle[i][2])
    V = [[min(all_x_coord), max(all_x_coord)], [min(all_y_coord), max(all_y_coord)], [min(all_z_coord), max(all_z_coord)]]
    return V


def terminate(T,V,max_triangle, max_depth):
    """
    Als boom niet meer verder moet opsplitsen True, anders False
    Op basis van maximaal aantal driehoeken in een leaf/ maximale diepte van boom
    :param T:
    :param V:
    :return: Boolean
    """

    # print("terminate?", len(T), V)
    if len(T) <= max_triangle or V[3] >= max_depth:
        return True
    for i in range(3):
        if V[i][0] == V[i][1]:
            return True
    else:
        return False


def new_leaf(T):
    """
    Maakt een leaf aan (eind node)
    :param T: lijst van driehoeken die in leaf horen
    :return: object leaf
    """
    leaf = Leaf(T)
    return leaf


def new_node(p, V, left_child, right_child):
    """
    Maakt een nieuwe node
    :param p: waarde waarop gesplitst is
    :param left_child: linkse tak
    :param right_child: rechtse tak
    :return: object node
    """
    node = Node(p, V, left_child,right_child)
    return node


def intersects_bounding_box(polygon, V, axis):
    for i in range(len(polygon)-2):
        if V[axis][0] <= polygon[i][axis] <= V[axis][1]:
            return True
    return False


def split(T, V, split_axis, split_axis_med):
    """
    Als de plaats van verdeling gekend is, verdeelt deze functie
     - V in Vleft en Vright
     - T in Tleft en Tright
    :param T: lijst van te verdelen driehoeken
    :param V: volume dat verdeeld moet worden
    :param split_axis: as op basis waarvan gesplitst wordt
    :param split_axis_med: waarde waarop gesplitst wordt
    :return: Vleft, Vright, Tleft, Tright
    """
    # for triangle in T:
    #     if not V[split_axis][0] <= triangle[4][split_axis] <= V[split_axis][1]:
    #         print("PROBLEMS")
    Vleft = copy.deepcopy(V)
    Vleft[split_axis][1] = split_axis_med
    Vleft[3] += 1
    Vright = copy.deepcopy(V)
    Vright[split_axis][0] = split_axis_med
    Vright[3] += 1
    Tleft = []
    Tright = []
    for triangle in T:
        if len(triangle) - 2 == 3:
            left = 0
            right = 0
            for i in range(len(triangle) - 2):
                if V[split_axis][0] == split_axis_med:
                    if Vleft[split_axis][0] <= triangle[i][split_axis] <= Vleft[split_axis][1]:
                        left += 1
                    else:
                        right += 1
                else:
                    if Vleft[split_axis][0] <= triangle[i][split_axis] < Vleft[split_axis][1]:
                        left += 1
                    elif Vright[split_axis][0] <= triangle[i][split_axis] <= Vright[split_axis][1]:
                        right += 1
            if left >= right:
                Tleft.append(triangle)
            elif right >= left:
                Tright.append(triangle)
        else:
            if intersects_bounding_box(triangle,Vleft, split_axis):
                Tleft.append(triangle)
            if intersects_bounding_box(triangle,Vright, split_axis):
                Tright.append(triangle)
    # print("all poly to 1 child?",len(Tleft),len(Tright))
    if len(T) == len(Tleft) or len(T) == len(Tright):
        Vleft[split_axis][0] = split_axis_med
        Vleft[split_axis][1] = split_axis_med
        Vright[split_axis][0] = split_axis_med
        Vright[split_axis][1] = split_axis_med
        Tleft = T[:int(len(T)/2)]
        Tright = T[int(len(T)/2):]
    # print(len(T), len(Tleft), len(Tright), V[split_axis], Vleft[split_axis], Vright[split_axis])
    # if len(T) == len(Tleft) or len(T) == len(Tright):
        # print(split_axis,split_axis_med)
        # for triangle in T:
            # print(triangle)
    return Vleft,Vright, Tleft, Tright


def calculate_median(T,V,axis):
    median_values = []
    # for i in range(len(T)):
    #     if V[axis][0] <= T[i][len(T[i]) - 1][axis] <= V[axis][1]:
    #         median_values[i] = T[i][len(T[i]) - 1][axis]
    #     else:
    #         mean = 0
    #         nb_inbox = 0
    #         for j in range(len(T[i]) - 2):
    #             if V[axis][0] <= T[i][j][axis] <= V[axis][1]:
    #                 mean += T[i][j][axis]
    #                 nb_inbox += 1
    #         # if nb_inbox == 0:
    #         #    print(T[i])
    #         #    print(V)
    #         #     print(axis)
    #         median_values[i] = mean/nb_inbox
    for i in range(len(T)):
        for j in range(len(T[i])-2):
            # print("point",T[i][j], axis)
            median_values.append(T[i][j][axis])
    median = np.median(np.array(median_values))
    # print("median", median)
    return median


def rec_build(T, V,max_triangles, max_depth):
    """
    Maakt kd-tree boom van ruimte V waarin driehoeken T bevinden
    :param T: lijst driehoeken
    (een driehoek heeft formaat [[x1, y1, z1],[x2,.....],[normaal],[zwaartepunt]]
    :param V: volume waarvan boom gemaakt wordt,
              vorm: [[xmin, xmax],[ymin, ymax],[zmin, zmax], diepte]
    :return: node
    """
    if terminate(T,V,max_triangles, max_depth):
        return new_leaf(T)
    split_axis = V[3] % 3
    split_axis_med = calculate_median(T,V,split_axis)
    V_left, V_right, T_left, T_right = split(T, V, split_axis, split_axis_med)
    return new_node(split_axis_med, V, rec_build(T_left, V_left,max_triangles, max_depth), rec_build(T_right, V_right,max_triangles, max_depth))


def add_center(T):
    for triangle in T:
        sum = np.zeros(3)
        for i in range(len(triangle)-1):
            sum += triangle[i]
        sum /= (len(triangle)-1)
        triangle.append(sum)
    return T


def join_triangles(triangles):
    points = dict()
    for triangle in triangles:
        for i in range(len(triangle) - 1):
            if tuple(triangle[i]) in points:
                points[tuple(triangle[i])] += 1
            else:
                points[tuple(triangle[i])] = 1
    polygon = []
    for point in points:
        if points[point] == 1 or points[point] == 2:
            polygon.append(point)
    polygon.append(triangles[0][3])
    return polygon


def prepare_T(objects,nb_triangles):
    T = []
    for obj in objects:
        if obj[:2] != "r_":
            for triangle in objects[obj]:
                T.append(triangle)
        elif obj[:4] != 'ext_':
            polygon = join_triangles(objects[obj])
            T.append(polygon)
    return T


def count_triangles(node, sum = 0):
    if isinstance(node,Leaf):
        sum += len(node.data)
        return sum
    else:
        sum += count_triangles(node.left_child)
        sum += count_triangles(node.right_child)
        return sum


def build_kdtree(objects, nb_triangles, max_triangles, max_depth):
    """
    Bouwt kd-tree van scene
    :param T: alle driehoeken
    :return: kd-boom
    """
    T = prepare_T(objects, nb_triangles)
    V = determine_max_coordinates(T)
    V.append(0)
    T = add_center(T)
    T = np.array(T)
    kdtree = rec_build(T,V,max_triangles, max_depth)
    # print(count_triangles(kdtree))
    # print("OBJECTS")
    # print(objects)
    # print("TREE")
    # print_tree(kdtree)
    return kdtree


def find_intersection(triangle, start_point, end_point):
    """
    zoekt of punten elkaar kunnen zien rond deze driehoek
    :param triangle: driehoeken in te onderzoeken leaf
    :param start_point: begin rechte
    :param end_point: einde rechte
    :return: 0 als niet zichtbaar en dus intersection, 1 als zichtbaar en dus geen intersectie
    """
    start_point = np.array(start_point)
    end_point = np.array(end_point)
    normal = np.array(triangle[len(triangle)-2])
    dire = end_point - start_point
    normal_dir = np.dot(normal, dire)
    small_number = 10**(-14)
    if (abs(np.linalg.norm(normal_dir)) < small_number):
        # print("case 1")
        return 1

    d = np.dot(normal, triangle[0])

    t = (d-np.dot(normal, start_point)) / normal_dir
    if (t<=0) or t>=1:
        # print("case 2")
        return 1
    intersection = start_point + t * dire

    for i in range(len(triangle)-2):
        edge = np.array(triangle[(i + 1) % (len(triangle) - 2)]) - np.array(triangle[i % (len(triangle) - 2)])
        vp = intersection - triangle[i % (len(triangle) - 2)]
        C = np.cross(edge,vp)
        if (np.dot(normal,C)<0):
            # print("case 3")
            return 1

    # print("case 6", triangle, start_point,end_point)
    return 0

def brute_visible(T,start_point, end_point):
    for triangle in T:
        visible = find_intersection(triangle,start_point,end_point)
        if not visible:
            return 0
    return 1

def visible(node ,start_point, end_point, depth = 0, checked = {}):
    """
    Bepaalt of start_point en end_point mutually visible zijn
    :param kdtree: boom van de scene (bestaat uit nodes gelinkt aan hun kinderen
    :param start_point: eerste punt
    :param end_point: tweede punt
    :return: 0 not visible of 1 visible
    """
    #print('conducting visible with', node.data, depth)
    mutual_visible = 1
    if isinstance(node, Leaf):
        # print("the node ", node, " with depth", depth, " is a leaf")
        # print(depth, len(node.data))
        for triangle in node.data:
            if tuple(map(tuple, triangle)) in checked:
                mutual_visible = checked[tuple(map(tuple, triangle))]
            else:
                mutual_visible = find_intersection(triangle, start_point, end_point)
                checked[tuple(map(tuple, triangle))] = mutual_visible
            if not mutual_visible:
                # print("found intersection in data of leaf")
                return 0
        else:
            # print("found no intersection in data of leaf")
            return 1
    else:
        # print(node)
        if start_point[depth%3] <= node.data or end_point[depth%3] <= node.data:
            # print("searching left_child")
            mutual_visible = visible(node.left_child,start_point, end_point, depth+1,checked)
            if not mutual_visible:
                # print("found intersection in left child")
                return 0
        # print(mutual_visible, node)
        # print(start_point[depth%3],node.data)
        if start_point[depth%3] >= node.data or end_point[depth%3] >= node.data:
            # print("searching right_child")
            mutual_visible = visible(node.right_child, start_point, end_point, depth+1,checked)
            if not mutual_visible:
                # print("found intersection in right child")
                return 0
        # print("survived left en right child searching and still going")
        if mutual_visible:
            # print("so just return 1")
            return 1



def print_tree(node,depth = 0):
    print("depth", depth)
    if isinstance(node, Node):
        print('Node')
        print(node.data)
        print_tree(node.left_child,depth+1)
        print_tree(node.right_child,depth+1)
    elif isinstance(node, Leaf):
        print('Leaf')
        print(len(node.data))
        print(node.data)


