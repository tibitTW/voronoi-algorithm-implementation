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
        return f"<Point>: ({self.x}, {self.y})"


class Line:
    def __init__(self, p1: Point, p2: Point) -> None:
        self.p1 = p1
        self.p2 = p2

    def __str__(self) -> str:
        return f"[{self.p1}, {self.p2}]"


class VD:
    def __init__(self, points=None, lines=None, convex_hull_points=None, inner_lines=None):
        self.points = points if points else []
        self.lines = lines if lines else {}
        self.convex_hull_points = convex_hull_points if convex_hull_points else []
        self.inner_lines = inner_lines if inner_lines else []

    def __str__(self) -> str:
        return "\n".join(
            (
                "= = = = = Voronoi Diagram: = = = = =",
                "points:",
                "\n".join([f"{p}" for p in self.points]),
                "lines:",
                "\n".join([f"{self.lines[key]}" for key in self.lines]),
                "convex hull points:",
                "\n".join([f"{p}" for p in self.convex_hull_points]),
                "inner lines:",
                "\n".join([f"{l}" for l in self.inner_lines]),
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
                "= = = = = Graph: = = = = =",
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
            )
        )


#################### mathematics functions ####################
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
        if p_tmp[0] < 0 or p_tmp[0] > 600 or p_tmp[1] < 0 or p_tmp[1] > 600:
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
        if p_tmp[0] < 0 or p_tmp[0] > 600 or p_tmp[1] < 0 or p_tmp[1] > 600:
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
    return Point(
        l2.p1.x + n * (l2.p2.x - l2.p1.x),
        l2.p1.y + n * (l2.p2.y - l2.p1.y),
    )


def get_2_vector_cos(v1: Point, v2: Point):
    return (v1.x * v2.x + v1.y * v2.y) / ((v1.x**2 + v1.y**2) ** 0.5 + (v2.x**2 + v2.y**2) ** 0.5)


#################### voronoi diagram algorithms ####################
def get_vd_steps(point_set):
    # records every step
    steps = []

    def merge_vd(left_vd: VD, right_vd: VD) -> VD:
        result_vd = VD(points=left_vd.points + right_vd.points)
        step_graph = Graph()

        hyperplane = []

        # TODO 找 left_vd 及 right_vd 的上下切線點
        left_top_idx = 0
        left_bottom_idx = 0
        right_top_idx = 0
        right_bottom_idx = 0

        # 找上切點
        is_loop = 2
        while is_loop:
            # TODO: corner case ()
            next_left_top_idx = (left_top_idx + 1) % len(left_vd.convex_hull_points)
            # 找到更好的切點
            if (right_vd.convex_hull_points[right_top_idx].y - left_vd.convex_hull_points[left_top_idx].y) / (
                right_vd.convex_hull_points[right_top_idx].x - left_vd.convex_hull_points[left_top_idx].x
            ) < (right_vd.convex_hull_points[right_top_idx].y - left_vd.convex_hull_points[next_left_top_idx].y) / (
                right_vd.convex_hull_points[right_top_idx].x - left_vd.convex_hull_points[next_left_top_idx].x
            ):
                left_top_idx = next_left_top_idx
                left_next = True
            else:
                left_next = False

            next_right_top_idx = (right_top_idx + 1) % len(right_vd.convex_hull_points)
            # 找到更好的切點
            if (left_vd.convex_hull_points[left_top_idx].y - right_vd.convex_hull_points[right_top_idx].y) / (
                left_vd.convex_hull_points[left_top_idx].x - right_vd.convex_hull_points[right_top_idx].x
            ) > (left_vd.convex_hull_points[left_top_idx].y - right_vd.convex_hull_points[next_right_top_idx].y) / (
                left_vd.convex_hull_points[left_top_idx].x - right_vd.convex_hull_points[next_right_top_idx].x
            ):
                right_top_idx = next_right_top_idx
                right_next = True
            else:
                right_next = False

            if not left_next and not right_next:
                is_loop -= 1
            else:
                is_loop = 2

        # 找下切點
        is_loop = 2
        while is_loop:
            # TODO: corner case ()
            next_left_bottom_idx = (left_bottom_idx + 1) % len(left_vd.convex_hull_points)
            # 找到更好的切點
            if (right_vd.convex_hull_points[right_bottom_idx].y - left_vd.convex_hull_points[left_bottom_idx].y) / (
                right_vd.convex_hull_points[right_bottom_idx].x - left_vd.convex_hull_points[left_bottom_idx].x
            ) > (right_vd.convex_hull_points[right_bottom_idx].y - left_vd.convex_hull_points[next_left_bottom_idx].y) / (
                right_vd.convex_hull_points[right_bottom_idx].x - left_vd.convex_hull_points[next_left_bottom_idx].x
            ):
                left_bottom_idx = next_left_bottom_idx
                left_next = True
            else:
                left_next = False

            next_right_bottom_idx = (right_bottom_idx + 1) % len(right_vd.convex_hull_points)
            # 找到更好的切點
            if (left_vd.convex_hull_points[left_bottom_idx].y - right_vd.convex_hull_points[right_bottom_idx].y) / (
                left_vd.convex_hull_points[left_bottom_idx].x - right_vd.convex_hull_points[right_bottom_idx].x
            ) < (left_vd.convex_hull_points[left_bottom_idx].y - right_vd.convex_hull_points[next_right_bottom_idx].y) / (
                left_vd.convex_hull_points[left_bottom_idx].x - right_vd.convex_hull_points[next_right_bottom_idx].x
            ):
                right_bottom_idx = next_right_bottom_idx
                right_next = True
            else:
                right_next = False

            if not left_next and not right_next:
                is_loop -= 1
            else:
                is_loop = 2

        # TODO 找 hyperplane

        # =============================== output results =============================== #
        step_graph.left_vd = left_vd
        step_graph.right_vd = right_vd
        step_graph.hyperplane = hyperplane

        steps.append(step_graph)

        # result_vd[(f"{left_vd[left_top_idx]}", f"{right_vd[right_top_idx]}")] = hyperplane[0]
        # result_vd[(f"{left_vd[left_bottom_idx]}", f"{right_vd[right_bottom_idx]}")] = hyperplane[-1]
        result_vd.convex_hull_points = (
            left_vd.convex_hull_points[: left_top_idx + 1]
            + right_vd.points[right_top_idx : right_bottom_idx + 1]
            + left_vd.convex_hull_points[left_bottom_idx:]
        )
        return result_vd

    def do_vd(point_set: list) -> VD:
        if len(point_set) == 1:
            return VD(points=point_set, convex_hull_points=point_set)

        # 兩點 voronoi
        if len(point_set) == 2:
            bisection_line = get_bisection_line(*point_set)

            result_vd = VD(points=point_set)
            result_vd.convex_hull_points = point_set
            result_vd.lines = {(f"{point_set[0]}", f"{point_set[1]}"): bisection_line}

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
                    (f"{point_set[0]}", f"{point_set[1]}"): bisection_line01,
                    (f"{point_set[1]}", f"{point_set[2]}"): bisection_line12,
                }
                result_vd.convex_hull_points = point_set

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
                outer_center.x > 600 or outer_center.x < 0 or outer_center.y > 600 or outer_center.y < 0
            ):
                result_vd = VD(points=point_set)
                step_graph = Graph(points=point_set)

                if max(squared_triangle_edges) == squared_triangle_edges[0]:
                    print("type: 3 points 2 lines ")
                    result_vd.lines = {
                        (f"{point_set[1]}", f"{point_set[2]}"): bisection_line12,
                        (f"{point_set[0]}", f"{point_set[2]}"): bisection_line02,
                    }

                elif max(squared_triangle_edges) == squared_triangle_edges[1]:
                    result_vd.lines = {
                        (f"{point_set[0]}", f"{point_set[1]}"): bisection_line01,
                        (f"{point_set[0]}", f"{point_set[2]}"): bisection_line02,
                    }

                elif max(squared_triangle_edges) == squared_triangle_edges[2]:
                    result_vd.lines = {
                        (f"{point_set[0]}", f"{point_set[1]}"): bisection_line01,
                        (f"{point_set[1]}", f"{point_set[2]}"): bisection_line12,
                    }

                result_vd.convex_hull_points = point_set
                step_graph.left_vd = result_vd

                # save steps
                steps.append(step_graph)
                return result_vd

            result_vd = VD(points=point_set, convex_hull_points=point_set)
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
                (f"{point_set[0]}", f"{point_set[1]}"): bisection_line01_tmp,
                (f"{point_set[1]}", f"{point_set[2]}"): bisection_line12_tmp,
                (f"{point_set[0]}", f"{point_set[2]}"): bisection_line02_tmp,
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
                    result_vd.lines[(f"{point_set[0]}", f"{point_set[1]}")] = bisection_line01_tmp

                # 最長邊為 12
                elif max(squared_triangle_edges) == squared_triangle_edges[1]:
                    bisection_line12_tmp = get_bisection_line(point_set[1], point_set[2])
                    # 判斷 12 邊要取哪段線段, cos() < 0 代表夾角較大，為正確方向
                    if get_2_vector_cos(bisection_line12_tmp.p1 - outer_center, e12_center - outer_center) < 0:
                        bisection_line12_tmp.p2 = outer_center
                    else:
                        bisection_line12_tmp.p1 = outer_center
                    result_vd.lines[(f"{point_set[1]}", f"{point_set[2]}")] = bisection_line12_tmp

                # 最長邊為 02
                elif max(squared_triangle_edges) == squared_triangle_edges[2]:
                    bisection_line02_tmp = get_bisection_line(point_set[0], point_set[2])
                    # 判斷 02 邊要取哪段線段, cos() < 0 代表夾角較大，為正確方向
                    if get_2_vector_cos(bisection_line02_tmp.p1 - outer_center, e02_center - outer_center) < 0:
                        bisection_line02_tmp.p2 = outer_center
                    else:
                        bisection_line02_tmp.p1 = outer_center
                    result_vd.lines[(f"{point_set[0]}", f"{point_set[2]}")] = bisection_line02_tmp

            step_graph.left_vd = result_vd
            # save steps
            steps.append(step_graph)
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
        print("there's no point")
        return [Graph()]
    elif len(point_set) == 1:
        print("there's only 1 point")
        return [Graph(point_set)]

    do_vd(point_set)

    return steps
