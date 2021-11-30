# point
import matplotlib.pyplot as plt


class VD:
    def __init__(self):
        self.points = []
        self.lines = []
        self.convexHullPoints = []


def get_squared_distance(p1, p2):
    return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2


# 找中垂線
def get_bisection(p1, p2):
    if p1[0] == p2[0]:  # 水平線
        y = (p1[1] + p2[1]) / 2
        return (0, y, 600, y)
    if p1[1] == p2[1]:  # 垂直線
        x = (p1[0] + p2[0]) / 2
        return (x, 0, x, 600)

    p3 = ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)
    v = (p1[1] - p2[1], p2[0] - p1[0])

    pA = (0, p3[1] - p3[0] * v[1] / v[0])
    pB = (p3[0] - p3[1] * v[0] / v[1], 0)
    pC = (600, p3[1] + (600 - p3[0]) * v[1] / v[0])
    pD = (p3[0] + (600 - p3[1]) * v[0] / v[1], 600)

    if v[0] * v[1] > 0:  # AB比，CD比
        dis_ac = get_squared_distance(pA, pC)
        dis_bc = get_squared_distance(pB, pC)
        dis_ad = get_squared_distance(pA, pD)
        if dis_ac < dis_bc:
            pS = pA
        else:
            pS = pB

        if dis_ac < dis_ad:
            pE = pC
        else:
            pE = pD

    else:  # BC比, AD比
        dis_ac = get_squared_distance(pA, pC)
        dis_bc = get_squared_distance(pB, pC)
        dis_dc = get_squared_distance(pD, pC)
        if dis_ac < dis_bc:
            pS = pC
        else:
            pS = pB
        dis_ad = get_squared_distance(pA, pD)
        if dis_ac < dis_dc:
            pE = pA
        else:
            pE = pD

    return (pS[0], pS[1], pE[0], pE[1])


def cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def intersect1D(a1: int, a2: int, b1: int, b2: int):
    a1, a2 = min(a1, a2), max(a1, a2)
    b1, b2 = min(b1, b2), max(b1, b2)

    return max(a1, b1) <= min(a2, b2)


def intersect(a1: list, a2: list, b1: list, b2: list):
    return (
        intersect1D(a1[0], a2[0], b1[0], b2[0])
        and intersect1D(a1[1], a2[1], b1[1], b2[1])
        and cross(a1, a2, b1) * cross(a1, a2, b2) <= 0
        and cross(b1, b2, a1) * cross(b1, b2, a2) <= 0
    )


def intersection(a1: list, a2: list, b1: list, b2: list):
    a = (a2[0] - a1[0], a2[1] - a1[1])
    b = (b2[0] - b1[0], b2[1] - b1[1])
    s = (b1[0] - a1[0], b1[1] - a1[1])

    cross_sb = cross((0, 0), s, b)
    cross_ab = cross((0, 0), a, b)
    return (a1[0] + a[0] * cross_sb / cross_ab, a1[1] + a[1] * cross_sb / cross_ab)
