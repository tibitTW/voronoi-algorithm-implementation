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
    def __init__(self, a_val=0, b_val=0) -> None:
        self._a = a_val
        self._b = b_val

    def __str__(self) -> str:
        return f"f(x) = {self._a} * x + {self._b}"

    # FIXME rename this function
    def get_val(self, x):
        return self._a * x + self._b

    def get_x_val(self, y):
        return (y - self.b) / self.a


# 找中垂線
# def get_bisection(p1: P, p2: P):
#     p3 = (p1 + p2) / 2
#     x_diff = p1.getX() - p2.getX()
#     y_diff = p1.getY() - p2.getY()
#     a = -x_diff / y_diff
#     b = p3.getY() - a * p3.getX()
#     return F(a, b)
def get_bisection(p1, p2):
    p3 = ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)
    x_diff = p1[0] - p2[0]
    y_diff = p1[1] - p2[1]
    if y_diff == 0:
        # TODO: 垂直線
        pass
    if x_diff and y_diff:
        a = -x_diff / y_diff
    elif 
    b = p3[1] - a * p3[0]
    return F(a, b)
