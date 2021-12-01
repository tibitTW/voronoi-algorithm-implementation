class VD:
    def __init__(self, points=None, lines=None):
        self.points = []
        self.convexHullPoints = set([])
        self.lines = []
        self.cuttedLines = []

        if points:
            self.points = points
        if lines:
            self.lines = lines


#################### mathematics functions ####################
def get_squared_distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return (x1 - x2) ** 2 + (y1 - y2) ** 2


# 找中垂線, 座標range(0, 600)
def get_bisection(p1, p2):
    x1, y1 = p1
    x2, y2 = p2

    if x1 == x2:  # 水平線
        y = (y1 + y2) / 2
        return (0, y, 600, y)

    if y1 == y2:  # 垂直線
        x = (x1 + x2) / 2
        return (x, 0, x, 600)

    x3, y3 = p3 = ((x1 + x2) / 2, (y1 + y2) / 2)
    vx, vy = v = (y1 - y2, x2 - x1)

    pA = (0, y3 - x3 * vy / vx)
    pB = (x3 - y3 * vx / vy, 0)
    pC = (600, y3 + (600 - x3) * vy / vx)
    pD = (x3 + (600 - p3[1]) * vx / vy, 600)

    if vx * vy > 0:  # AB比，CD比
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

    return (*pS, *pE)


def cross(o, a, b):
    ax, ay = a
    bx, by = b
    ox, oy = 0
    return (ax - ox) * (by - oy) - (ay - oy) * (bx - ox)


def intersect1D(a1, a2, b1, b2):
    a1, a2 = min(a1, a2), max(a1, a2)
    b1, b2 = min(b1, b2), max(b1, b2)

    return max(a1, b1) <= min(a2, b2)


def intersect(a1, a2, b1, b2):
    return (
        intersect1D(a1[0], a2[0], b1[0], b2[0])
        and intersect1D(a1[1], a2[1], b1[1], b2[1])
        and cross(a1, a2, b1) * cross(a1, a2, b2) <= 0
        and cross(b1, b2, a1) * cross(b1, b2, a2) <= 0
    )


def intersection(a1, a2, b1, b2):
    a = (a2[0] - a1[0], a2[1] - a1[1])
    b = (b2[0] - b1[0], b2[1] - b1[1])
    s = (b1[0] - a1[0], b1[1] - a1[1])

    cross_sb = cross((0, 0), s, b)
    cross_ab = cross((0, 0), a, b)
    return (a1[0] + a[0] * cross_sb / cross_ab, a1[1] + a[1] * cross_sb / cross_ab)


#################### voronoi diagram algorithms ####################
def do_vd(contents):
    points = contents["points"]
    if len(points) <= 1:
        return
    elif len(points) == 2:
        bisection = get_bisection(*points)
        contents["lines"].append(bisection)
        return contents
    else:
        vd = get_vd()
        return {"points": vd.points, "lines": vd.lines}


def get_vd(points):
    if len(points) <= 1:
        return VD(points=points)
    if len(points) == 2:
        bisection = get_bisection(*points)
        return VD(points=points, lines=[bisection])

    left_vd = get_vd(points[0 : len(points) // 2])
    right_vd = get_vd(points[len(points) // 2 :])
    merged_vd = merge_vd(left_vd, right_vd)
    return merged_vd


# TODO
def merge_vd(left_vd, right_vd):
    res_vd = VD()
    return res_vd
