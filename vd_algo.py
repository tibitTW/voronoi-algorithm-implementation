class Point:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"


class Line:
    def __init__(self, p1: Point, p2: Point) -> None:
        self.p1 = p1
        self.p2 = p2

    def __str__(self) -> str:
        return f"[{self.p1}, {self.p2}]"


class Graph:
    def __init__(self, points: list = None, lines: list = None, left_vd_lines: list = None, right_vd_lines: list = None, hyperplane: Line = None) -> None:
        self.points = points if points else []
        self.lines = lines if lines else []
        self.left_vd_lines = left_vd_lines if left_vd_lines else []
        self.right_vd_lines = right_vd_lines if right_vd_lines else []
        self.hyperplane = hyperplane if hyperplane else None

    def __str__(self) -> str:
        return "\n".join(
            [
                "= = = = = Graph: = = = = =",
                "points:",
                "\n".join([f"{p}" for p in self.points]),
                "lines:",
                "\n".join([f"{l}" for l in self.lines]),
            ]
        )


class VD:
    def __init__(self, points=None, lines=None, inner_points=None, inner_lines=None):
        self.points = points if points else []
        self.lines = lines if lines else []
        self.inner_points = inner_points if inner_points else []
        self.inner_lines = inner_lines if inner_lines else []

    def __str__(self) -> str:
        return "\n".join(
            (
                "= = = = = Voronoi Diagram: = = = = =",
                f"points: {self.points}",
                f"lines: {self.lines}",
                f"inner_points: {self.inner_points}",
                f"inner_lines: {self.inner_lines}",
            )
        )


#################### mathematics functions ####################

#################### voronoi diagram algorithms ####################
def get_vd_steps(point_set):
    if len(point_set) == 0:
        return [Graph()]
    elif len(point_set) == 1:
        return [Graph(point_set)]

    # saves every step
    steps = []

    # TODO
    def merge_vd(left_vd, right_vd) -> VD:
        result_vd = VD()

        # save steps: left_vd, right_vd, hyperplane in graph
        steps.append(result_vd)

        return result_vd

    # TODO
    def do_vd(point_set) -> VD:
        if len(point_set) == 0:
            steps.append(Graph())
            return
        elif len(point_set) == 1:
            steps.append(Graph(point_set))
            return

        left_points = point_set[: len(point_set) // 2]
        right_points = point_set[len(point_set) // 2 :]
        left_vd = do_vd(left_points)
        right_vd = do_vd(right_points)

        result_vd = merge_vd(left_vd, right_vd)
        return result_vd

    do_vd(point_set)

    return steps
