""" $LAN=Python$ """

"""license: copyright of M103040083 李峮驊"""

import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd

import copy


# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = #
# = = = = = = = = = = = = = vd_algo.py  = = = = = = = = = = = = = = #
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = #

CANVAS_SIZE = 600

# ============================= data structure ============================= #
class Point:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def __add__(self, p):
        return Point(self.x + p.x, self.y + p.y)

    def __sub__(self, p):
        return Point(self.x - p.x, self.y - p.y)

    def __eq__(self, __o: object) -> bool:
        return self.x == __o.x and self.y == __o.y

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def __repr__(self) -> str:
        return f"<Point>: {self.__str__()}"


class Line:
    def __init__(self, p1: Point, p2: Point) -> None:
        self.p1 = p1 if type(p1) == Point else Point(*p1)
        self.p2 = p2 if type(p2) == Point else Point(*p2)

    def __str__(self) -> str:
        return f"[{self.p1}, {self.p2}]"

    def __repr__(self) -> str:
        return f"<Line>: {self.__str__()}"


class VD:
    def __init__(self, points=None, lines=None, CH_points=None):
        self.points = points if points else []
        self.lines = lines if lines else {}
        self.CH_points = CH_points if CH_points else []

    def __str__(self) -> str:
        return "\n".join(
            (
                "= = = = = Voronoi Diagram: = = = = =",
                "points:",
                "\n".join([f"{p}" for p in self.points]),
                "lines:",
                "\n".join([f"{self.lines[key]}" for key in self.lines]),
                "convex hull points:",
                "\n".join([f"{p}" for p in self.CH_points]),
            )
        )


class Graph:
    def __init__(self, points: list = None, lines: list = None, left_vd: VD = None, right_vd: VD = None, hyperplane: list = None) -> None:
        self.points = points if points else []
        self.lines = lines if lines else {}
        self.left_vd = left_vd if left_vd else None
        self.right_vd = right_vd if right_vd else None
        self.hyperplane = hyperplane if hyperplane else []

    def __str__(self) -> str:
        return "\n".join(
            (
                "= = = = = = = = = = = = = Graph: = = = = = = = = = = = = =",
                "points:",
                "\n".join([f"{p}" for p in self.points]),
                "lines:",
                "\n".join([f"{self.lines[key]}" for key in self.lines]),
                "left vd:",
                f"{self.left_vd}",
                "right vd:",
                f"{self.right_vd}",
                "hyperline:",
                "\n".join([f"{l}" for l in self.hyperplane]),
                "\n",
            )
        )


# ===================================== mathematics functions ===================================== #
def get_squared_p2p_distance(p1: Point, p2: Point) -> float:
    return (p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2


def get_bisection_line(p1: Point, p2: Point) -> Line:
    center_point = ((p1.x + p2.x) / 2, (p1.y + p2.y) / 2)
    line_vector = (p1.y - p2.y, p2.x - p1.x)

    # get point 1 that outside the canvas
    step = 0
    while True:
        step += 1
        p_tmp = (
            center_point[0] + step * line_vector[0],
            center_point[1] + step * line_vector[1],
        )
        if p_tmp[0] < 0 or p_tmp[0] > CANVAS_SIZE or p_tmp[1] < 0 or p_tmp[1] > CANVAS_SIZE:
            break
    line_p1 = Point(
        center_point[0] + step * line_vector[0],
        center_point[1] + step * line_vector[1],
    )

    # get point 2 that outside the canvas
    step = 0
    while True:
        step -= 1
        p_tmp = (
            center_point[0] + step * line_vector[0],
            center_point[1] + step * line_vector[1],
        )
        if p_tmp[0] < 0 or p_tmp[0] > CANVAS_SIZE or p_tmp[1] < 0 or p_tmp[1] > CANVAS_SIZE:
            break
    line_p2 = Point(
        center_point[0] + step * line_vector[0],
        center_point[1] + step * line_vector[1],
    )

    return Line(line_p1, line_p2)


def get_concurrent(l1: Line, l2: Line) -> Point:
    n = ((l2.p1.y - l1.p1.y) * (l1.p2.x - l1.p1.x) - (l2.p1.x - l1.p1.x) * (l1.p2.y - l1.p1.y)) / (
        (l2.p2.x - l2.p1.x) * (l1.p2.y - l1.p1.y) - (l2.p2.y - l2.p1.y) * (l1.p2.x - l1.p1.x)
    )
    concurrent = Point(
        l2.p1.x + n * (l2.p2.x - l2.p1.x),
        l2.p1.y + n * (l2.p2.y - l2.p1.y),
    )

    return concurrent


def get_2_vector_cos(v1: Point, v2: Point):
    return (v1.x * v2.x + v1.y * v2.y) / ((v1.x**2 + v1.y**2) ** 0.5 + (v2.x**2 + v2.y**2) ** 0.5)


def cross(po, pa, pb):
    return (pa.x - po.x) * (pb.y - po.y) - (pa.y - po.y) * (pb.x - po.x)


# ===================================== voronoi diagram algorithms ===================================== #
def get_vd_steps(point_set):
    # records every step
    steps = []

    def merge_vd(left_vd: VD, right_vd: VD) -> VD:
        left_vd = copy.deepcopy(left_vd)
        right_vd = copy.deepcopy(right_vd)

        result_vd = VD(points=left_vd.points + right_vd.points)
        step_graph = Graph()

        hyperplane = []

        # = = = = = = = = = = = = 找 left_vd 及 right_vd 的上下切線點 = = = = = = = = = = = =  #

        left_CH_points_tmp = [p for p in left_vd.CH_points]
        # sort points
        left_CH_points_tmp.sort(key=lambda p: p.y)
        left_CH_points_tmp.sort(key=lambda p: p.x)

        right_CH_points_tmp = [p for p in right_vd.CH_points]
        # sort points
        right_CH_points_tmp.sort(key=lambda p: p.y)
        right_CH_points_tmp.sort(key=lambda p: p.x)

        left_top_idx = left_bottom_idx = 0
        while left_vd.CH_points[left_top_idx] != left_CH_points_tmp[-1]:
            left_top_idx += 1
            left_bottom_idx += 1

        right_top_idx = right_bottom_idx = right_rightest_idx = 0
        while right_vd.CH_points[right_rightest_idx] != right_CH_points_tmp[-1]:
            right_rightest_idx += 1

        # 找上切點
        left_top_is_meet = right_top_is_meet = False
        while not (left_top_is_meet and right_top_is_meet):
            left_top_idx_next = left_top_idx - 1
            if left_top_idx_next < 0:
                left_top_idx_next = len(left_vd.CH_points) - 1

            if (
                cross(
                    right_vd.CH_points[right_top_idx],
                    left_vd.CH_points[left_top_idx],
                    left_vd.CH_points[left_top_idx_next],
                )
                > 0
            ):
                left_top_idx = left_top_idx_next
                left_top_is_meet = False
            else:
                left_top_is_meet = True

            right_top_idx_next = right_top_idx + 1
            if right_top_idx_next >= len(right_vd.CH_points):
                right_top_idx_next = 0
            if (
                cross(
                    left_vd.CH_points[left_top_idx],
                    right_vd.CH_points[right_top_idx],
                    right_vd.CH_points[right_top_idx_next],
                )
                < 0
            ):
                right_top_idx = right_top_idx_next
                left_top_is_meet = False
                right_top_is_meet = False
            else:
                right_top_is_meet = True

        # 找下切點
        left_bottom_is_meet = right_bottom_is_meet = False
        while not (left_bottom_is_meet and right_bottom_is_meet):
            left_bottom_idx_next = left_bottom_idx + 1
            if left_bottom_idx_next >= len(left_vd.CH_points):
                left_bottom_idx_next = 0

            if (
                cross(
                    right_vd.CH_points[right_bottom_idx],
                    left_vd.CH_points[left_bottom_idx],
                    left_vd.CH_points[left_bottom_idx_next],
                )
                < 0
            ):
                left_bottom_idx = left_bottom_idx_next
                left_bottom_is_meet = False
            else:
                left_bottom_is_meet = True

            right_bottom_idx_next = right_bottom_idx - 1
            if right_bottom_idx_next < 0:
                right_bottom_idx_next = len(right_vd.CH_points) - 1
            if (
                cross(
                    left_vd.CH_points[left_bottom_idx],
                    right_vd.CH_points[right_bottom_idx],
                    right_vd.CH_points[right_bottom_idx_next],
                )
                > 0
            ):
                right_bottom_idx = right_bottom_idx_next
                left_bottom_is_meet = False
                right_bottom_is_meet = False
            else:
                right_bottom_is_meet = True

        # ============================= TODO 找 hyperplane ============================= #
        left_i = left_top_idx
        left_i_next = left_i + 1
        if left_i_next >= len(left_vd.CH_points):
            left_i_next = 0

        right_i = right_top_idx
        right_i_next = right_i - 1
        if right_i_next < 0:
            right_i_next = len(right_vd.CH_points) - 1

        hyperplanes = {}
        hyperplane_line_tmp = get_bisection_line(left_vd.CH_points[left_i], right_vd.CH_points[right_i])
        hyperplane_line_tmp_key = (str(left_vd.CH_points[left_i]), str(right_vd.CH_points[right_i]))

        # switch 2 points, makes p1 always upper than p2
        if (hyperplane_line_tmp.p1.y > hyperplane_line_tmp.p2.y) or (
            (hyperplane_line_tmp.p1.y == hyperplane_line_tmp.p2.y) and (hyperplane_line_tmp.p1.x > hyperplane_line_tmp.p2.x)
        ):
            hyperplane_line_tmp.p1, hyperplane_line_tmp.p2 = hyperplane_line_tmp.p2, hyperplane_line_tmp.p1

        last_concurrent = hyperplane_line_tmp.p1
        has_next_concorrent = True

        ii = 0
        iter_i = 0
        while has_next_concorrent and iter_i < 50:
            iter_i += 1

            # find left_line & right_line
            for key in left_vd.lines:
                if (str(left_vd.CH_points[left_i]) in key) and (str(left_vd.CH_points[left_i_next]) in key):
                    left_line_key = key
                    break
            for key in right_vd.lines:
                if (str(right_vd.CH_points[right_i]) in key) and (str(right_vd.CH_points[right_i_next]) in key):
                    right_line_key = key
                    break

            left_concorrent = get_concurrent(left_vd.lines[left_line_key], hyperplane_line_tmp)
            right_concorrent = get_concurrent(right_vd.lines[right_line_key], hyperplane_line_tmp)

            print("last_concorrent:", last_concurrent)
            print("left_concorrent:", left_concorrent)
            print("right_concorrent:", right_concorrent)
            print()

            has_left_concorrent = (
                (0 <= left_concorrent.x <= CANVAS_SIZE) and (0 <= left_concorrent.y <= CANVAS_SIZE) and (last_concurrent.y < left_concorrent.y)
            )
            has_right_concorrent = (
                (0 <= right_concorrent.x <= CANVAS_SIZE) and (0 <= right_concorrent.y <= CANVAS_SIZE) and (last_concurrent.y < right_concorrent.y)
            )

            print("has_left_concorrent:", has_left_concorrent)
            print("has_right_concorrent:", has_right_concorrent)
            print()

            if (not has_left_concorrent) and (not has_right_concorrent):
                print("do none")
                has_next_concorrent = False
            elif has_left_concorrent and has_right_concorrent:
                squared_left_distance = get_squared_p2p_distance(last_concurrent, left_concorrent)
                squared_right_distance = get_squared_p2p_distance(last_concurrent, right_concorrent)

                print("squared_left_distance:", squared_left_distance)
                print("squared_right_distance:", squared_right_distance)

                if squared_left_distance < squared_right_distance:
                    print("shorter is left")
                    print()
                    # update last_concorrent
                    last_concurrent = left_concorrent

                    # 切 hyperplane
                    hyperplane_line_tmp.p2 = left_concorrent

                    # 存 hyperplane
                    hyperplanes[hyperplane_line_tmp_key] = hyperplane_line_tmp

                    # 找下一條 hyperplnae
                    hyperplane_line_tmp = get_bisection_line(left_vd.CH_points[left_i_next], right_vd.CH_points[right_i])
                    hyperplane_line_tmp_key = (str(left_vd.CH_points[left_i_next]), str(right_vd.CH_points[right_i]))

                    # cut left line
                    left_line = left_vd.lines[left_line_key]
                    if left_line.p1.x > left_line.p2.x:
                        left_line.p1, left_line.p2 = left_line.p2, left_line.p1
                    left_line.p2 = left_concorrent

                    # update cutted left line
                    left_vd.lines[left_line_key] = left_line

                    # update left idx
                    left_i = left_i_next
                    left_i_next += 1
                    if left_i_next >= len(left_vd.CH_points):
                        left_i_next = 0

                elif squared_left_distance > squared_right_distance:
                    print("shorter is right")
                    print()
                    # update last_concorrent
                    last_concurrent = right_concorrent

                    # 切 hyperplane
                    hyperplane_line_tmp.p2 = right_concorrent

                    # 存 hyperplane
                    hyperplanes[hyperplane_line_tmp_key] = hyperplane_line_tmp

                    # 找下一條 hyperplnae
                    hyperplane_line_tmp = get_bisection_line(left_vd.CH_points[left_i], right_vd.CH_points[right_i_next])
                    hyperplane_line_tmp_key = (str(left_vd.CH_points[left_i]), str(right_vd.CH_points[right_i_next]))

                    # cut right line
                    right_line = right_vd.lines[right_line_key]
                    if right_line.p1.x > right_line.p2.x:
                        right_line.p1, right_line.p2 = right_line.p2, right_line.p1
                    right_line.p1 = right_concorrent

                    # update cutted right line
                    right_vd.lines[right_line_key] = right_line

                    # update right idx
                    right_i = right_i_next
                    right_i_next -= 1
                    if right_i_next < 0:
                        right_i_next = len(right_vd.CH_points) - 1

                else:
                    hyperplane_line_tmp.p2 = left_concorrent
                    hyperplanes[(*hyperplane_line_tmp_key, ii)] = hyperplane_line_tmp
                    ii += 1

                    hyperplane_line_tmp = get_bisection_line(
                        left_vd.CH_points[left_i_next],
                        right_vd.CH_points[right_i_next],
                    )

                    last_concurrent = left_concorrent

                    # cut left line
                    left_line = left_vd.lines[left_line_key]
                    if left_line.p1.x > left_line.p2.x:
                        left_line.p1, left_line.p2 = left_line.p2, left_line.p1
                    left_line.p2 = left_concorrent
                    left_vd.lines[left_line_key] = left_line

                    # update left idx
                    left_i = left_i_next
                    left_i_next += 1
                    if left_i_next >= len(left_vd.CH_points):
                        left_i_next = 0

                    # cut right line
                    right_line = right_vd.lines[right_line_key]
                    if right_line.p1.x > right_line.p2.x:
                        right_line.p1, right_line.p2 = right_line.p2, right_line.p1
                    right_line.p1 = right_concorrent
                    right_vd.lines[right_line_key] = right_line

                    # update right idx
                    right_i = right_i_next
                    right_i_next -= 1
                    if right_i_next < 0:
                        right_i_next = len(right_vd.CH_points) - 1

            elif has_left_concorrent:
                print("left")
                print()
                # update last_concorrent
                last_concurrent = left_concorrent

                # 切 hyperplane
                hyperplane_line_tmp.p2 = left_concorrent

                # 存 hyperplane
                hyperplanes[hyperplane_line_tmp_key] = hyperplane_line_tmp

                # 找下一條 hyperplnae
                hyperplane_line_tmp = get_bisection_line(left_vd.CH_points[left_i_next], right_vd.CH_points[right_i])
                hyperplane_line_tmp_key = (str(left_vd.CH_points[left_i_next]), str(right_vd.CH_points[right_i]))

                # cut left line
                left_line = left_vd.lines[left_line_key]
                if left_line.p1.x > left_line.p2.x:
                    left_line.p1, left_line.p2 = left_line.p2, left_line.p1
                left_line.p2 = left_concorrent

                # update cutted left line
                left_vd.lines[left_line_key] = left_line

                # update left idx
                left_i = left_i_next
                left_i_next += 1
                if left_i_next >= len(left_vd.CH_points):
                    left_i_next = 0

            elif has_right_concorrent:
                print("right")
                print()
                # update last_concorrent
                last_concurrent = right_concorrent

                # 切 hyperplane
                hyperplane_line_tmp.p2 = right_concorrent

                # 存 hyperplane
                hyperplanes[hyperplane_line_tmp_key] = hyperplane_line_tmp

                # 找下一條 hyperplnae
                hyperplane_line_tmp = get_bisection_line(left_vd.CH_points[left_i], right_vd.CH_points[right_i_next])
                hyperplane_line_tmp_key = (str(left_vd.CH_points[left_i]), str(right_vd.CH_points[right_i_next]))

                # cut right line
                right_line = right_vd.lines[right_line_key]
                if right_line.p1.x > right_line.p2.x:
                    right_line.p1, right_line.p2 = right_line.p2, right_line.p1
                right_line.p1 = right_concorrent

                # update cutted right line
                right_vd.lines[right_line_key] = right_line

                # update right idx
                right_i = right_i_next
                right_i_next -= 1
                if right_i_next < 0:
                    right_i_next = len(right_vd.CH_points) - 1

            # switch 2 points, makes p1 always upper than p2
            if (hyperplane_line_tmp.p1.y > hyperplane_line_tmp.p2.y) or (
                (hyperplane_line_tmp.p1.y == hyperplane_line_tmp.p2.y) and (hyperplane_line_tmp.p1.x > hyperplane_line_tmp.p2.x)
            ):
                hyperplane_line_tmp.p1, hyperplane_line_tmp.p2 = hyperplane_line_tmp.p2, hyperplane_line_tmp.p1

            hyperplane_line_tmp.p1 = last_concurrent

        hyperplane_line_tmp = get_bisection_line(left_vd.CH_points[left_bottom_idx], right_vd.CH_points[right_bottom_idx])
        # switch 2 points, makes p1 always upper than p2
        if hyperplane_line_tmp.p1.y > hyperplane_line_tmp.p2.y:
            hyperplane_line_tmp.p1, hyperplane_line_tmp.p2 = hyperplane_line_tmp.p2, hyperplane_line_tmp.p1

        hyperplane_line_tmp.p1 = last_concurrent
        hyperplanes[hyperplane_line_tmp_key] = hyperplane_line_tmp

        # =============================== output results =============================== #
        step_graph.left_vd = left_vd
        step_graph.right_vd = right_vd
        step_graph.hyperplane = hyperplanes

        steps.append(step_graph)

        result_vd.lines = {**left_vd.lines, **right_vd.lines, **result_vd.lines, **hyperplanes}

        # update convex hull points of result voronoi diagram
        result_vd.CH_points = []
        result_vd.CH_points += left_vd.CH_points[: left_top_idx + 1]
        if right_top_idx > right_bottom_idx:
            result_vd.CH_points += right_vd.CH_points[right_top_idx:] + right_vd.CH_points[: right_bottom_idx + 1]
        else:
            result_vd.CH_points += right_vd.CH_points[right_top_idx : right_bottom_idx + 1]
        if left_bottom_idx != 0:
            result_vd.CH_points += left_vd.CH_points[left_bottom_idx:]

        step_graph = Graph(left_vd=result_vd)
        steps.append(step_graph)

        print()
        print("------------------------------------------")
        print()

        return result_vd

    def do_vd(point_set: list) -> VD:
        if len(point_set) == 1:
            return VD(points=point_set, CH_points=point_set)

        # 兩點 voronoi
        if len(point_set) == 2:
            bisection_line = get_bisection_line(*point_set)

            result_vd = VD(points=point_set)
            result_vd.CH_points = point_set
            result_vd.lines = {(str(point_set[0]), str(point_set[1])): bisection_line}

            step_graph = Graph(points=point_set)
            step_graph.left_vd = result_vd

            # save steps
            steps.append(step_graph)
            return result_vd

        # 三點 voronoi
        if len(point_set) == 3:
            # corner case: 共線
            if (
                (point_set[0].x == point_set[1].x and point_set[1].x == point_set[2].x)
                or (point_set[0].y == point_set[1].y and point_set[1].y == point_set[2].y)
                or (
                    (point_set[0].x != point_set[1].x)
                    and (point_set[1].x != point_set[2].x)
                    and (point_set[2].y - point_set[1].y) / (point_set[2].x - point_set[1].x)
                    == (point_set[1].y - point_set[0].y) / (point_set[1].x - point_set[0].x)
                )
            ):
                bisection_line01 = get_bisection_line(point_set[0], point_set[1])
                bisection_line12 = get_bisection_line(point_set[1], point_set[2])

                result_vd = VD(points=point_set)
                result_vd.lines = {
                    (str(point_set[0]), str(point_set[1])): bisection_line01,
                    (str(point_set[1]), str(point_set[2])): bisection_line12,
                }
                result_vd.CH_points = point_set

                step_graph = Graph(points=point_set)
                step_graph.left_vd = result_vd

                # save steps
                steps.append(step_graph)
                return result_vd

            # = = = = = = = = = = = = = = = = = = 順時針排序 = = = = = = = = = = = = = = = = = = #
            if point_set[0].x == point_set[1].x:
                point_set = [point_set[0], point_set[2], point_set[1]]
            elif point_set[0].x != point_set[2].x:
                slope_01 = (point_set[1].y - point_set[0].y) / (point_set[1].x - point_set[0].x)
                slope_02 = (point_set[2].y - point_set[0].y) / (point_set[2].x - point_set[0].x)

                # point1 比 point2 低
                if slope_01 > slope_02:
                    point_set = [point_set[0], point_set[2], point_set[1]]

            # for p in point_set:
            #     print(p)

            # print("--------------")

            # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = #

            bisection_line01 = get_bisection_line(point_set[0], point_set[1])
            bisection_line12 = get_bisection_line(point_set[1], point_set[2])
            bisection_line02 = get_bisection_line(point_set[0], point_set[2])

            outer_center = get_concurrent(bisection_line01, bisection_line12)

            squared_triangle_edges = (
                (point_set[0].x - point_set[1].x) ** 2 + (point_set[0].y - point_set[1].y) ** 2,
                (point_set[1].x - point_set[2].x) ** 2 + (point_set[1].y - point_set[2].y) ** 2,
                (point_set[0].x - point_set[2].x) ** 2 + (point_set[0].y - point_set[2].y) ** 2,
            )

            # = = = = = = = = = = = = 鈍角三角形且外心超出畫面，只要畫兩條線 = = = = = = = = = = = = #
            if (sum(squared_triangle_edges) // max(squared_triangle_edges) < 2) and (
                outer_center.x > CANVAS_SIZE or outer_center.x < 0 or outer_center.y > CANVAS_SIZE or outer_center.y < 0
            ):
                result_vd = VD(points=point_set)
                step_graph = Graph(points=point_set)

                if max(squared_triangle_edges) == squared_triangle_edges[0]:
                    # print("type: 3 points 2 lines ")
                    result_vd.lines = {
                        (str(point_set[1]), str(point_set[2])): bisection_line12,
                        (str(point_set[0]), str(point_set[2])): bisection_line02,
                    }

                elif max(squared_triangle_edges) == squared_triangle_edges[1]:
                    result_vd.lines = {
                        (str(point_set[0]), str(point_set[1])): bisection_line01,
                        (str(point_set[0]), str(point_set[2])): bisection_line02,
                    }

                elif max(squared_triangle_edges) == squared_triangle_edges[2]:
                    result_vd.lines = {
                        (str(point_set[0]), str(point_set[1])): bisection_line01,
                        (str(point_set[1]), str(point_set[2])): bisection_line12,
                    }

                result_vd.CH_points = point_set
                step_graph.left_vd = result_vd

                # save steps
                steps.append(step_graph)
                return result_vd

            result_vd = VD(points=point_set, CH_points=point_set)
            step_graph = Graph(points=point_set)

            bisection_line01_tmp = get_bisection_line(point_set[0], point_set[1])
            bisection_line12_tmp = get_bisection_line(point_set[1], point_set[2])
            bisection_line02_tmp = get_bisection_line(point_set[0], point_set[2])

            e01_center = Point((point_set[0].x + point_set[1].x) / 2, (point_set[0].y + point_set[1].y) / 2)
            e12_center = Point((point_set[1].x + point_set[2].x) / 2, (point_set[1].y + point_set[2].y) / 2)
            e02_center = Point((point_set[0].x + point_set[2].x) / 2, (point_set[0].y + point_set[2].y) / 2)

            # 判斷 01 邊要取哪段線段, cos() < 0 代表夾角較大，為正確方向
            if get_2_vector_cos(bisection_line01.p1 - outer_center, e01_center - outer_center) > 0:
                bisection_line01_tmp.p2 = outer_center
            else:
                bisection_line01_tmp.p1 = outer_center

            # 判斷 12 邊要取哪段線段, cos() < 0 代表夾角較大，為正確方向
            if get_2_vector_cos(bisection_line12.p1 - outer_center, e12_center - outer_center) > 0:
                bisection_line12_tmp.p2 = outer_center
            else:
                bisection_line12_tmp.p1 = outer_center

            # 判斷 02 邊要取哪段線段, cos() < 0 代表夾角較大，為正確方向
            if get_2_vector_cos(bisection_line02.p1 - outer_center, e02_center - outer_center) > 0:
                bisection_line02_tmp.p2 = outer_center
            else:
                bisection_line02_tmp.p1 = outer_center

            result_vd.lines = {
                (str(point_set[0]), str(point_set[1])): bisection_line01_tmp,
                (str(point_set[1]), str(point_set[2])): bisection_line12_tmp,
                (str(point_set[0]), str(point_set[2])): bisection_line02_tmp,
            }
            # = = = = = = = = = = = = = = = = = = = 鈍角三角形 = = = = = = = = = = = = = = = = = = = #
            if sum(squared_triangle_edges) // max(squared_triangle_edges) < 2:
                # 最長邊為 01
                if max(squared_triangle_edges) == squared_triangle_edges[0]:
                    bisection_line01_tmp = get_bisection_line(point_set[0], point_set[1])
                    # 判斷 01 邊要取哪段線段, cos() < 0 代表夾角較大，為正確方向
                    if get_2_vector_cos(bisection_line01_tmp.p1 - outer_center, e01_center - outer_center) < 0:
                        bisection_line01_tmp.p2 = outer_center
                    else:
                        bisection_line01_tmp.p1 = outer_center
                    result_vd.lines[(str(point_set[0]), str(point_set[1]))] = bisection_line01_tmp

                # 最長邊為 12
                elif max(squared_triangle_edges) == squared_triangle_edges[1]:
                    bisection_line12_tmp = get_bisection_line(point_set[1], point_set[2])
                    # 判斷 12 邊要取哪段線段, cos() < 0 代表夾角較大，為正確方向
                    if get_2_vector_cos(bisection_line12_tmp.p1 - outer_center, e12_center - outer_center) < 0:
                        bisection_line12_tmp.p2 = outer_center
                    else:
                        bisection_line12_tmp.p1 = outer_center
                    result_vd.lines[(str(point_set[1]), str(point_set[2]))] = bisection_line12_tmp

                # 最長邊為 02
                elif max(squared_triangle_edges) == squared_triangle_edges[2]:
                    bisection_line02_tmp = get_bisection_line(point_set[0], point_set[2])
                    # 判斷 02 邊要取哪段線段, cos() < 0 代表夾角較大，為正確方向
                    if get_2_vector_cos(bisection_line02_tmp.p1 - outer_center, e02_center - outer_center) < 0:
                        bisection_line02_tmp.p2 = outer_center
                    else:
                        bisection_line02_tmp.p1 = outer_center
                    result_vd.lines[(str(point_set[0]), str(point_set[2]))] = bisection_line02_tmp

            step_graph.left_vd = result_vd
            # save steps
            steps.append(step_graph)

            # print(result_vd)

            return result_vd

        left_points = point_set[: len(point_set) // 2]
        right_points = point_set[len(point_set) // 2 :]
        left_vd = do_vd(left_points)
        right_vd = do_vd(right_points)

        result_vd = merge_vd(left_vd, right_vd)
        return result_vd

    # sort points
    point_set.sort(key=lambda p: p.y)
    point_set.sort(key=lambda p: p.x)

    # remove repeat points
    pi = 0
    while pi < len(point_set) - 1:
        if (point_set[pi].x == point_set[pi + 1].x) and (point_set[pi].y == point_set[pi + 1].y):
            point_set.pop(pi)
        else:
            pi += 1

    if len(point_set) == 0:
        # print("there's no point")
        return [Graph()]
    elif len(point_set) == 1:
        # print("there's only 1 point")
        return [Graph(point_set)]

    do_vd(point_set)

    return steps


# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = #
# = = = = = = = = = = = = = file_process.py = = = = = = = = = = = = #
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = #

# 開測資
def load_dataset() -> list:

    filetypes = {("input files", "*.in"), ("all files", "*.*")}
    filename = fd.askopenfilename(title="選取檔案", initialdir="./", filetypes=filetypes)

    with open(filename, "r", encoding="utf-8") as f:
        data = f.read()

    data = data.strip().split("\n")

    dataset = []
    i = 0
    while i < len(data):

        # empty line & comment line
        if not data[i] or data[i][0] == "#":
            i += 1
        elif data[i] == "0":
            break
        else:
            set_size = int(data[i])
            i += 1
            pi = 0
            points = []
            while pi < set_size:
                if data[i] and data[i][0] != "#":
                    x, y = map(int, data[i].split(" "))
                    p_tmp = Point(x, y)
                    points.append(p_tmp)

                pi += 1
                i += 1

            dataset.append(points)

    print("Dataset loaded.")
    for set_i, s in enumerate(dataset):
        print(f"set {set_i+1}")
        for p in s:
            print(p)
        print("---------------")
    return dataset


def open_vd_graph() -> Graph:
    filename = fd.askopenfilename(
        title="選取檔案",
        initialdir="./",
        filetypes={
            ("all files", "*.*"),
            ("voronoi diagram files", "*.vd"),
        },
    )

    with open(filename, "r") as f:
        data = f.read()

    data = data.strip().split("\n")

    points = []
    lines = []
    for line in data:
        # read points
        if line[0] == "P":
            ptmp = tuple(map(int, line[2:].split(" ")))
            points.append(ptmp)
        # read lines
        elif line[0] == "E":
            ltmp = tuple(map(int, line[2:].split(" ")))
            lines.append(ltmp)
        else:
            print("format error!")

    return Graph(points, lines)


def save_vd_graph(graph: Graph):
    print(graph)

    # ================ sorting ================ #
    graph.points.sort(key=lambda p: p.y)
    graph.points.sort(key=lambda p: p.x)

    graph.lines.sort(key=lambda l: l.p2.y)
    graph.lines.sort(key=lambda l: l.p2.x)
    graph.lines.sort(key=lambda l: l.p1.y)
    graph.lines.sort(key=lambda l: l.p1.x)
    # ========================================= #

    f = fd.asksaveasfile(
        mode="w",
        defaultextension=".vd",
        filetypes={
            ("voronoi diagram files", "*.vd"),
            ("all files", "*.*"),
        },
    )

    if f is None:
        print("file saving failed")
        return

    for p in graph.points:
        f.write(f"P {p.x:.0f} {p.y:.0f}\n")

    for l in graph.lines:
        f.write(f"E {l.p1.x:.0f} {l.p1.y:.0f} {l.p2.x:.0f} {l.p2.y:.0f}\n")

    f.close()


# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = #
# = = = = = = = = = = = = = = = main.py = = = = = = = = = = = = = = #
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = #


class sc:
    def __init__(self) -> None:
        # main window
        self.root = Tk()
        self.root.title("Voronoi Algorithm")
        # key binding
        self.root.bind("<Key>", self.key_event)
        # self.root.bind("<KeyPress>", self.key_event)
        # self.root.bind("<KeyRelease>", self.key_event)

        # main frame
        self.mainframe = ttk.Frame(self.root, padding="10 10 10 10")
        self.mainframe.grid(column=0, row=0)

        # main canvas
        self.canvas = Canvas(self.mainframe, width=600, height=600, background="white")
        self.canvas.bind("<Button-1>", self.canvas_mouse_click_event)
        self.canvas.grid(column=0, row=0)

        # frame including buttons
        self.sideframe = ttk.Frame(self.root, padding="0 10 10 10")
        self.sideframe.grid(column=1, row=0)
        self.init_sideframe_elements()
        self.init_sideframe_layout()

        # store all points and lines on screen
        self.current_graph = Graph()
        # store point data read from file
        self.dataset = []
        self.dataset_idx = 0

        # store every step of doing voronoi diagram by divide and conquer methods
        self.solution_steps = []
        self.steps_idx = 0

    #################### core functions ####################
    def init_sideframe_elements(self):
        self.dataset_idx_str = StringVar()
        self.dataset_idx_lb = ttk.Label(self.sideframe, textvariable=self.dataset_idx_str)
        self.load_file_btn = ttk.Button(self.sideframe, width=16, text="load dataset", command=self.read_dataset)
        self.show_next_set_btn = ttk.Button(self.sideframe, width=16, text="next set (n)", command=self.show_next_set)
        self.step_by_step_btn = ttk.Button(self.sideframe, width=16, text="step by step (s)", command=self.step_by_step)
        self.run_btn = ttk.Button(self.sideframe, width=16, text="run (r)", command=self.do_voronoi)
        self.save_graph_file_btn = ttk.Button(self.sideframe, width=16, text="save graph", command=self.save_graph)
        self.load_graph_file_btn = ttk.Button(self.sideframe, width=16, text="load graph", command=self.load_graph)
        self.clear_canvas_btn = ttk.Button(self.sideframe, width=16, text="clear canvas (c)", command=self.clean_all)

    def init_sideframe_layout(self):
        self.dataset_idx_lb.grid(row=0)
        self.load_file_btn.grid(row=1)
        self.show_next_set_btn.grid(row=2)
        self.run_btn.grid(row=3)
        self.step_by_step_btn.grid(row=4)
        self.save_graph_file_btn.grid(row=5)
        self.load_graph_file_btn.grid(row=6)
        self.clear_canvas_btn.grid(row=7)

    def canvas_mouse_click_event(self, event):
        p_tmp = Point(event.x, event.y)
        self.print_point(p_tmp.x, p_tmp.y)
        self.current_graph.points.append(p_tmp)
        # print(f"new point at: {p_tmp}")
        self.solution_steps = []
        self.steps_idx = 0

    def mainloop(self):
        self.root.mainloop()

    #################### file processing ####################
    def read_dataset(self):
        self.dataset = load_dataset()
        self.dataset_idx = 0

        self.clean_all()
        self.current_graph = Graph(self.dataset[self.dataset_idx])
        self.print_graph(Graph(self.dataset[self.dataset_idx]))
        self.dataset_idx_str.set(f"Set [{self.dataset_idx+1}/{len(self.dataset)}]")

    def save_graph(self):
        save_vd_graph(self.current_graph)

    def load_graph(self):
        self.clean_all()
        self.current_graph = open_vd_graph()
        self.print_graph(self.current_graph)

    ####################### graphing ######################
    def clear_canvas(self):
        self.canvas.delete("all")

    def print_point(self, x: int, y: int, r: int = 3, fill="white", outline="black"):
        self.canvas.create_oval(x - r, y - r, x + r, y + r, fill=fill, outline=outline)

    def print_line(self, x1: int, y1: int, x2: int, y2: int, fill="black", line_type=None):
        if line_type == "ch_line":
            self.canvas.create_line(
                x1,
                y1,
                x2,
                y2,
                fill="grey",
                # arrow=tk.LAST,
                dash=(2, 2),
            )
            return
        self.canvas.create_line(x1, y1, x2, y2, fill=fill)

    def print_graph(self, graph: Graph):
        # print(graph)
        if graph.points:
            for p in graph.points:
                self.print_point(p.x, p.y)

        if graph.lines:
            if type(graph.lines) == list:
                for l in graph.lines:
                    self.print_line(l.p1.x, l.p1.y, l.p2.x, l.p2.y)
            if type(graph.lines) == dict:
                for key in graph.lines:
                    self.print_line(
                        graph.lines[key].p1.x,
                        graph.lines[key].p1.y,
                        graph.lines[key].p2.x,
                        graph.lines[key].p2.y,
                    )

        # draw the left voronoi diagram
        if graph.left_vd:
            for p in graph.left_vd.points:
                self.print_point(p.x, p.y, fill="red", outline="red")

            self.print_point(graph.left_vd.CH_points[0].x, graph.left_vd.CH_points[0].y, r=10, fill="", outline="red")
            for i in range(-1, len(graph.left_vd.CH_points) - 1):
                self.print_line(
                    graph.left_vd.CH_points[i].x,
                    graph.left_vd.CH_points[i].y,
                    graph.left_vd.CH_points[i + 1].x,
                    graph.left_vd.CH_points[i + 1].y,
                    line_type="ch_line",
                )

            for key in graph.left_vd.lines:
                self.print_line(
                    graph.left_vd.lines[key].p1.x,
                    graph.left_vd.lines[key].p1.y,
                    graph.left_vd.lines[key].p2.x,
                    graph.left_vd.lines[key].p2.y,
                    fill="red",
                )

        # draw the right voronoi diagram
        if graph.right_vd:
            for p in graph.right_vd.points:
                self.print_point(p.x, p.y, fill="blue", outline="blue")

            self.print_point(graph.right_vd.CH_points[0].x, graph.right_vd.CH_points[0].y, r=10, fill="", outline="blue")
            for i in range(-1, len(graph.right_vd.CH_points) - 1):
                self.print_line(
                    graph.right_vd.CH_points[i].x,
                    graph.right_vd.CH_points[i].y,
                    graph.right_vd.CH_points[i + 1].x,
                    graph.right_vd.CH_points[i + 1].y,
                    line_type="ch_line",
                )

            for key in graph.right_vd.lines:
                self.print_line(
                    graph.right_vd.lines[key].p1.x,
                    graph.right_vd.lines[key].p1.y,
                    graph.right_vd.lines[key].p2.x,
                    graph.right_vd.lines[key].p2.y,
                    fill="blue",
                )

        if graph.hyperplane:

            for key in graph.hyperplane:
                self.print_line(graph.hyperplane[key].p1.x, graph.hyperplane[key].p1.y, graph.hyperplane[key].p2.x, graph.hyperplane[key].p2.y, fill="green")

    ######################## others ########################
    def clean_all(self):
        self.clear_canvas()
        self.clear_contents()
        self.solution_steps = []
        self.steps_idx = 0

    def clear_contents(self):
        self.current_graph = Graph()

    def show_next_set(self):
        if len(self.dataset) == 0:
            print("no dataset!")
            return
        self.dataset_idx += 1
        if self.dataset_idx >= len(self.dataset):
            self.dataset_idx = 0

        self.current_graph = Graph(self.dataset[self.dataset_idx])
        self.clear_canvas()
        self.print_graph(self.current_graph)
        self.dataset_idx_str.set(f"Set [{self.dataset_idx+1}/{len(self.dataset)}]")
        self.solution_steps = []

    def do_voronoi(self):
        self.solution_steps = get_vd_steps(self.current_graph.points)
        self.clear_canvas()
        self.print_graph(self.solution_steps[-1])
        self.steps_idx = 0

    def step_by_step(self):
        if not self.solution_steps:
            self.solution_steps = get_vd_steps(self.current_graph.points)
            self.steps_idx = 0

            # print(self.solution_steps)

        self.clear_canvas()
        self.print_graph(self.solution_steps[self.steps_idx])

        # print(self.solution_steps[self.steps_idx].left_vd.CH_points)

        self.steps_idx += 1
        if self.steps_idx >= len(self.solution_steps):
            self.steps_idx = 0

    def key_event(self, event):
        if event.char == "n":
            self.show_next_set()
        elif event.char == "r":
            self.do_voronoi()
        elif event.char == "q":
            self.root.quit()
        elif event.char == "c":
            self.clean_all()
        elif event.char == "s":
            self.step_by_step()


if __name__ == "__main__":
    main_sc = sc()

    main_sc.mainloop()
