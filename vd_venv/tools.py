class VD:
    def __init__(self, points=None, lines=None, CH_points=None, CH_lines=None):
        self.points = []
        self.CH_points = []
        self.lines = []
        self.CH_lines = []

        if points:
            self.points = points
        if lines:
            self.lines = lines
        if CH_points:
            self.CH_points = CH_points
        if CH_lines:
            self.CH_lines = CH_lines

    def __str__(self) -> str:
        return f"VD: points: {self.points},\nlines: {self.lines},\nCH_points: {self.CH_points},\nCH_lines: {self.CH_lines}"


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
    ox, oy = o
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
def do_vd(points):
    def get_vd(points):

        if len(points) <= 1:
            return VD(
                points=points,
                CH_points=points,
            )
        if len(points) == 2:
            bisection = get_bisection(*points)
            return VD(
                points=list(points),
                CH_points=list(points),
                lines=[bisection],
            )

        left_vd = get_vd(points[0 : len(points) // 2])
        right_vd = get_vd(points[len(points) // 2 :])
        return merge_vd(left_vd, right_vd)

    def merge_vd(left_vd, right_vd):
        if len(left_vd.points) <= 2 and len(right_vd.points) <= 2:
            if len(left_vd.points) == 1 and len(right_vd.points) == 1:  # [1, 1]
                bisection = get_bisection(left_vd.points[0], right_vd.points[0])

                res_vd = VD(
                    points=left_vd.points + right_vd.points,
                    CH_points=left_vd.points + right_vd.points,
                    lines=[bisection],
                    CH_lines=[bisection],
                )
                return res_vd

            elif len(left_vd.points) == 1:  # [1, 2]
                left_p = left_vd.points[0]
                right_p1, right_p2 = right_vd.points
                # 判斷右側哪個點是上點
                if cross(left_p, right_p1, right_p2) <= 0:
                    right_top = right_p2
                    right_bottom = right_p1
                else:
                    right_top = right_p1
                    right_bottom = right_p2

                if right_top == right_p1:
                    CH_points = [left_p, right_p1, right_p2]
                else:
                    CH_points = [left_p, right_p2, right_p1]

                # 畫中垂線
                hyperplane = []
                a1x, a1y, a2x, a2y = bisection1 = get_bisection(left_p, right_top)
                b1x, b1y, b2x, b2y = bisection2 = get_bisection(left_p, right_bottom)
                a1, a2 = (a1x, a1y), (a2x, a2y)
                b1, b2 = (b1x, b1y), (b2x, b2y)
                if intersect(a1, a2, b1, b2):
                    ox, oy = intersection(a1, a2, b1, b2)
                    if a1y < oy:
                        hyperplane.append((a1x, a1y), (ox, oy))
                    if a2y > oy:
                        hyperplane.append((a2x, a2y), (ox, oy))

                    hyperplane = [intersection(a1, a2, b1, b2)]

                res_vd = VD(
                    points=left_vd.points + right_vd.points,
                    CH_points=CH_points,
                )
                return res_vd

            else:  # [2,2]
                left_p1, left_p2 = left_vd.points
                right_p1, right_p2 = right_vd.points

                CH_points = [left_p1]
                points = [left_p2, right_p1, right_p2]
                point_o = current_point = left_p1

                while points:
                    top_point = points[0]
                    for p in points[1:]:
                        if cross(current_point, top_point, p) <= 0:
                            top_point = p
                    if cross(current_point, point_o, top_point) > 0:
                        break
                    current_point = top_point
                    CH_points.append(top_point)
                    points.remove(top_point)

                res_vd = VD(
                    points=left_vd.points + right_vd.points,
                    CH_points=CH_points,
                )

                return res_vd

        res_vd = VD(points=left_vd.points + right_vd.points)

        left_p = left_vd.points[-1]
        right_p = right_vd.points[0]

        # = = = = = = = = = = = = = 找上緣點 = = = = = = = = = = = = = #
        left_top_idx = left_vd.CH_points.index(left_p)
        right_top_idx = right_vd.CH_points.index(right_p)
        left_top_idx_next = left_top_idx - 1
        right_top_idx_next = right_top_idx + 1

        if left_top_idx_next < 0:
            left_top_idx_next = len(left_vd.CH_points) - 1
        if right_top_idx_next > len(right_vd.CH_points) - 1:
            right_top_idx_next = 0

        left_limit, right_limit, is_meet_limit = False, False, False
        while not is_meet_limit:
            if cross(left_vd.CH_points[left_top_idx], right_vd.CH_points[right_top_idx], right_vd.CH_points[right_top_idx_next]) < 0:
                right_top_idx = right_top_idx_next
                right_top_idx_next += 1
                if right_top_idx_next > len(right_vd.CH_points) - 1:
                    right_top_idx_next = 0
                right_limit = False
            else:
                right_limit = True

            if cross(right_vd.CH_points[right_top_idx], left_vd.CH_points[left_top_idx], left_vd.CH_points[left_top_idx_next]) > 0:
                left_top_idx = left_top_idx_next
                left_top_idx_next -= 1
                if left_top_idx_next < 0:
                    left_top_idx_next = len(left_vd.CH_points) - 1
                left_limit = False
            else:
                left_limit = True

            is_meet_limit = left_limit and right_limit

        # = = = = = = = = = = = = = 找下緣點 = = = = = = = = = = = = = #
        left_bottom_idx = left_vd.CH_points.index(left_p)
        right_bottom_idx = right_vd.CH_points.index(right_p)
        left_bottom_idx_next = left_bottom_idx + 1
        right_bottom_idx_next = right_bottom_idx - 1

        if left_bottom_idx_next >= len(left_vd.CH_points):
            left_bottom_idx_next = 0
        if right_bottom_idx_next < 0:
            right_bottom_idx_next = len(right_vd.CH_points) - 1

        left_limit, right_limit, is_meet_limit = False, False, False
        while not is_meet_limit:
            if cross(left_vd.CH_points[left_bottom_idx], right_vd.CH_points[right_bottom_idx], right_vd.CH_points[right_bottom_idx_next]) > 0:
                right_bottom_idx = right_bottom_idx_next
                right_bottom_idx_next -= 1
                if right_bottom_idx_next < 0:
                    right_bottom_idx_next = len(right_vd.CH_points) - 1

                right_limit = False
            else:
                right_limit = True

            if cross(right_vd.CH_points[right_bottom_idx], left_vd.CH_points[left_bottom_idx], left_vd.CH_points[left_bottom_idx_next]) < 0:
                left_bottom_idx = left_bottom_idx_next
                left_bottom_idx_next += 1
                if left_bottom_idx_next >= len(left_vd.CH_points):
                    left_bottom_idx_next = 0
                left_limit = False
            else:
                left_limit = True

            is_meet_limit = left_limit and right_limit

        res_vd.CH_points = left_vd.CH_points[: left_top_idx + 1]
        if right_top_idx > right_bottom_idx:
            res_vd.CH_points += right_vd.CH_points[right_top_idx:] + right_vd.CH_points[: right_bottom_idx + 1]
        else:
            res_vd.CH_points += right_vd.CH_points[right_top_idx : right_bottom_idx + 1]

        if left_bottom_idx != 0:
            res_vd.CH_points += left_vd.CH_points[left_bottom_idx:]

        return res_vd

    if len(points) <= 1:
        return [VD(points=points, CH_points=points)]
    elif len(points) == 2:
        bisection = get_bisection(*points)
        return [VD(points=list(points), CH_lines=[bisection], CH_points=list(points))]
    else:
        get_vd(points)
        solutions = [get_vd(points)]
        return solutions
