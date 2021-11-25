# point
import matplotlib.pyplot as plt


class P:
    def __init__(self, x=0, y=0) -> None:
        self._x = x
        self._y = y

    def __str__(self) -> str:
        return f"P({self._x}, {self._y})"

    def setX(self, val):
        self._x = val

    def setY(self, val):
        self._y = val

    def setPos(self, x_val=None, y_val=None):
        if x_val:
            self._x = x_val
        if y_val:
            self._y = y_val

    def getX(self):
        return self._x

    def getY(self):
        return self._y

    def getPos(self):
        return (self._x, self._y)

    # FIXME needs to update after implement in tkinter
    def draw(self, c="k"):
        plt.scatter(self._x, self._y, c=c)

    def __add__(self, P2):
        return P(self._x + P2._x, self._y + P2._y)

    def __sub__(self, P2):
        return P(self.x - P2._x, self._y - P2._y)

    def __truediv__(self, n):
        x = self._x / n
        y = self._y / n

        if self._x % n == 0:
            x = int(x)
        if self._y % n == 0:
            y = int(y)

        return P(x, y)


# line
class L:
    def __init__(self, p1, p2) -> None:
        if type(p1) == P:
            x1, y1 = p1.getPos()
        else:
            x1, y1 = p1
        if type(p2) == P:
            x2, y2 = p2.getPos()
        else:
            x2, y2 = p2

        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2

    def __str__(self) -> str:
        return f"L({self._x1}, {self._y1}) -> ({self._x2}, {self._y2})"

    def setPos(self, p1, p2):
        if type(p1) == P:
            x1, y1 = p1.getPos()
        else:
            x1, y1 = p1
        if type(p2) == P:
            x2, y2 = p2.getPos()
        else:
            x2, y2 = p2

        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2

    def setP1(self, p1):
        if type(p1) == P:
            x1, y1 = p1.getPos()
        self._x1 = x1
        self._y1 = y1

    def setP2(self, p2):
        if type(p2) == P:
            x2, y2 = p2.getPos()
        else:
            x2, y2 = p2
        self._x2 = x2
        self._y2 = y2


class F:
    def __init__(self, a=0, b=0, c=0) -> None:
        self._a = a
        self._b = b
        self._c = c

    def __str__(self) -> str:
        return f"function: {self._a}x + {self._b}y = {self._c}"

    def get_y_val(self, x):
        return (self._c - self._a * x) / self._b

    def get_x_val(self, y):
        return (self._c - self._b * y) / self._a

    # FIXME rename this function
    def get_val(self, x):
        return self._a * x + self._b


# 找中垂線
def get_bisection(p1, p2):
    if p1[0] == p2[0]:  # 水平線
        y = (p1[1] + p2[1]) / 2
        return 0, y, 600, y
    if p1[1] == p2[1]:  # 垂直線
        x = (p1[0] + p2[0]) / 2
        return x, 0, x, 600

    p3 = ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)
    v = (p1[1] - p2[1], p2[0] - p1[0])

    pA = (0, p3[1] - p3[0] * v[1] / v[0])
    pB = (p3[0] - p3[1] * v[0] / v[1], 0)
    pC = (600, p3[1] + (600 - p3[0]) * v[1] / v[0])
    pD = (p3[0] + (600 - p3[1]) * v[0] / v[1], 600)

    if v[0] * v[1] < 0:  # BC比, AD比
        if pB[0] < 0 or pB[0] > 600:
            pS = pC
        else:
            pS = pB
        if pA[0] < 0 or pA[0] > 600:
            pE = pD
        else:
            pE = pA
    else:  # AB比，CD比
        if pA[0] < 0 or pA[0] > 600:
            pS = pB
        else:
            pS = pA
        if pC[0] < 0 or pC[0] > 600:
            pE = pD
        else:
            pE = pC

    return pS[0], pS[1], pE[0], pE[1]


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
