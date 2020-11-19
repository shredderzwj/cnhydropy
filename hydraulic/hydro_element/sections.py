import math
from operator import itemgetter


class BaseSection(object):
    """断面基类"""
    def breadth(self, h: float):
        """水面宽"""
        raise NotImplementedError('breadth 方法必须被重写')

    def area(self, h: float):
        """过水断面面积"""
        raise NotImplementedError('area 方法必须被重写')

    def perimeter(self, h: float):
        """湿周"""
        raise NotImplementedError('perimeter 方法必须被重写')

    def radius(self, h: float):
        """水力半径"""
        return self.area(h) / self.perimeter(h)

    def element(self, h: float):
        """水力要素计算结果"""
        return {
            'h': h,
            'B': self.breadth(h),       # 水面宽
            'A': self.area(h),          # 过水断面面积
            'X': self.perimeter(h),     # 湿周
            'R': self.radius(h),        # 水力半径
        }

    def manning(self, h: float, n: float, j: float):
        """
        曼宁公式，计算过流能力
        :param h: float 水深（水位）
        :param n: float 糙率
        :param j: float 比降
        :return: {"C": 谢才系数, 'Q': 设计流量, 'V': 平均流速}
        """
        if not hasattr(self, 'element'):
            raise NotImplementedError('element 方法必须被定义')
        element = self.element(h)
        R = element.get("R")
        A = element.get("A")
        C = 1 / n * R ** (1 / 6)
        V = C * math.sqrt(R * j)
        Q = A * V
        return {
            **element,
            "C": C,
            "V": V,
            "Q": Q,
        }


class TrapezoidalSection(BaseSection):
    """梯形断面"""
    def __init__(self, m: float, b: float):
        """
        :param m: float 边坡系数
        :param b: float 底宽
        """
        self.m = m
        self.b = b

    def area(self, h: float):
        return h * (self.b + self.m * h)

    def breadth(self, h: float):
        return self.b + 2*h*self.m

    def perimeter(self, h: float):
        self.b + 2*h*math.pow(1 + self.m ** 2, 0.5)


class DuplexSection(BaseSection):
    """复式断面"""
    def __init__(self, m1: float, m2: float, b1: float, b2: float, h1: float):
        """
        :param m1: float 底部边坡系数
        :param m2: float 上部边坡系数
        :param b1: float 下部梯形底宽
        :param b2: float 上部梯形底宽
        :param h1: float 下部梯形高
        """
        self.m1 = m1
        self.m2 = m2
        self.b1 = b1
        self.b2 = b2
        self.h1 = h1

    def breadth(self, h: float):
        if h <= self.h1:
            return self.b1 + 2*self.m1*h
        return self.b2 + 2*self.m2*(h - self.h1)

    def area(self, h: float):
        if h <= self.h1:
            return h*(self.b1 + self.m1*h)
        return self.h1*(self.b1+self.m1*self.h1) + (h - self.h1) *\
               (self.b2 + self.m2 * (h - self.h1))

    def perimeter(self, h: float):
        if h <= self.h1:
            return self.b1 + 2*h * math.sqrt(1 + self.m1 ** 2)
        return self.b2 - 2*self.m1*self.h1 + 2*self.h1*math.sqrt(1 + self.m1**2)\
                + 2*(h - self.h1)*math.sqrt(1+self.m2**2)


class USection(BaseSection):
    """U形断面"""
    def __init__(self, r: float, m: float):
        """
        :param r: float 底部弧形半径
        :param m: 上部边坡系数
        """
        self.r = r
        self.m = m
        self.theta = 2 * math.atan2(1, m)
        self.b = 2 * r / math.sqrt(1 + m**2)
        self.h1 = r * (1 - m / math.sqrt(1 + m**2))

    def alpha(self, h: float):
        """湿周所占弧形角度"""
        return 2 * math.acos((self.r - h) / self.r)

    def area(self, h: float):
        if h <= self.h1:
            return self.r**2 * (self.alpha(h) - math.sin(self.alpha(h))) / 2
        return self.r**2 * (self.theta - self.m / (1 + self.m**2)) / 2\
                + (self.b + 2 * self.m * (h - self.h1)) * (h - self.h1)

    def perimeter(self, h: float):
        if h <= self.h1:
            return self.r * self.alpha(h)
        return self.r * self.theta + 2 * (h - self.h1) * math.sqrt(1 + self.m**2)

    def breadth(self, h: float):
        if h <= self.h1:
            return 2 * math.sqrt(2*h*self.r - h**2)
        return self.b + 2*self.m*(h - self.h1)


class CircleSection(BaseSection):
    """圆形断面"""

    def __init__(self, r: float):
        """
        :param r: float 圆形断面半径
        """
        self.r = r

    def theta(self, h: float):
        """湿周所占弧形角度"""
        return 2 * math.acos((self.r - h) / self.r)

    def breadth(self, h: float):
        return 2 * math.sqrt(h * (2 * self.r - h))

    def area(self, h: float):
        theta = self.theta(h)
        self.r ** 2 * (theta - math.sin(theta)) / 2

    def perimeter(self, h: float):
        return self.r * self.theta(h)


class ParabolaSection(BaseSection):
    """抛物线形断面"""
    def __init__(self, h: float, b: float):
        """
        :param h: float 断面深
        :param b: float 断面宽
                以上两个参数确定抛物线形状
        """
        self.h = h
        self.b = b

    def area(self, h: float):
        return 2 / 3 * self.breadth(h) * h

    def perimeter(self, h: float):
        return math.sqrt((1 + 4*h) * h) + 0.5 * math.log(
            2 * math.sqrt(h) + math.sqrt(1 + 4*h), math.e)

    def breadth(self, h: float):
        return self.b * math.sqrt(h / self.h)


class MeasuredSection(BaseSection):
    """实测断面"""
    def __init__(self, coords):
        """
        :param coords: list(list) 实测坐标点[(x1, y1), (x2, y2) ...]
        """
        self.coords = sorted(coords, key=itemgetter(0))

    def area(self, h: float):
        return self.element(h).get('A')

    def perimeter(self, h: float):
        return self.element(h).get('X')

    def breadth(self, h: float):
        return self.element(h).get('B')

    def element(self, h: float):
        x, y = list(zip(*self.coords))
        if h < min(y):
            print('水位低于河底！')
            raise ValueError
        if h > max(y):
            print('水位高于堤顶！')
            raise ValueError
        s = 0
        ka = 0
        b = 0
        for i in range(0, len(x) - 1):
            if y[i] != y[i + 1]:
                x0 = (h - y[i]) * (x[i + 1] - x[i]) / (y[i + 1] - y[i]) + x[i]
            else:
                x0 = x[i + 1]
            s1 = (h - y[i + 1]) * (x[i + 1] - x0) / 2
            s2 = (h - y[i]) * (x0 - x[i]) / 2
            s3 = (2 * h - y[i] - y[i + 1]) * (x[i + 1] - x[i]) / 2
            ka1 = ((x[i + 1] - x0) ** 2 + (y[i + 1] - h) ** 2) ** 0.5
            ka2 = ((x[i] - x0) ** 2 + (y[i] - h) ** 2) ** 0.5
            ka3 = ((x[i] - x[i + 1]) ** 2 + (y[i] - y[i + 1]) ** 2) ** 0.5
            b1 = x[i + 1] - x0
            b2 = x0 - x[i]
            b3 = x[i + 1] - x[i]
            if y[i] >= h > y[i + 1] or y[i] > h >= y[i + 1]:
                s += s1
                ka += ka1
                b += b1
            elif y[i] <= h < y[i + 1] or y[i] < h <= y[i + 1]:
                s += s2
                ka += + ka2
                b += b2
            elif h > y[i] and h > y[i + 1]:
                s += s3
                ka += ka3
                b += b3

        return {
            'h': h - min(y),
            'B': b,  # 水面宽
            'A': s,  # 过水断面面积
            'X': ka,  # 湿周
            'R': s / ka if ka != 0 else 0,  # 水力半径
        }

        

