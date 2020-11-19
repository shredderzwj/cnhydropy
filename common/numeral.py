# -*- coding:utf-8 -*-
# 数学计算相关模块

from math import fabs, sqrt, cos, sin, acos, copysign


def sheng_jin(a, b=0.0, c=0.0, d=0.0):
    """
    盛金公式解一元三次方程
    :param a:  float -> 三次项系数
    :param b:  float -> 二次项系数
    :param c:  float -> 一次项系数
    :param d:  float -> 常数项系数
    :return:  list -> 根 [[根1， 误差], [根2，误差], [根3， 误差]]
    """
    # 误差数
    eps = 1e-15
    # 数据处理
    if a == 0:
        print('三次项系数不能为0')
        raise ValueError

    # 重根判别式
    A = b ** 2 - 3 * a * c
    B = b * c - 9 * a * d
    C = c ** 2 - 3 * b * d

    # 总判别式
    delta = B ** 2 - 4 * A * C

    # Case1，当A=B=C时，三个相等的实根。
    if (fabs(A - B) < eps) and (fabs(A - C) < eps):
        X1 = - b / 3 / a
        X2 = - b / 3 / a
        X3 = - b / 3 / a
    else:
        # Case2， 一实根，两个共轭复根
        if delta > eps:
            Y1 = A * b + 3 * a * ((- B + sqrt(delta)) / 2)
            Y2 = A * b + 3 * a * ((- B - sqrt(delta)) / 2)
            imag = (sqrt(3) / 2 * (
                        copysign(fabs(Y1) ** (1 / 3), Y1) - copysign(fabs(Y2) ** (1 / 3),
                                                                     Y2))) / 3 / a
            real_ = (- b + (copysign(fabs(Y1) ** (1 / 3), Y1) + copysign(fabs(Y2) ** (1 / 3),
                                                                         Y2)) / 2) / 3 / a
            X1 = (- b - (copysign(fabs(Y1) ** (1 / 3), Y1) + copysign(fabs(Y2) ** (1 / 3),
                                                                      Y2))) / 3 / a
            X2 = complex(real_, imag)
            X3 = complex(real_, -imag)

        # case3 三个不同实根
        elif delta < -eps:
            T = (2 * A * b - 3 * a * B) / 2 / A ** 1.5
            seita = acos(T)
            X1 = (- b - 2 * sqrt(A) * cos(seita / 3)) / 3 / a
            X2 = (- b + sqrt(A) * (cos(seita / 3) + sqrt(3) * sin(seita / 3))) / 3 / a
            X3 = (- b + sqrt(A) * (cos(seita / 3) - sqrt(3) * sin(seita / 3))) / 3 / a

        # case4 三个实根，其中有一个二重根
        else:
            K = B / A
            X1 = - b / a + K
            X2 = - K / 2
            X3 = - K / 2

    dy1 = a * X1 ** 3 + b * X1 ** 2 + c * X1 + d
    dy2 = a * X2 ** 3 + b * X2 ** 2 + c * X2 + d
    dy3 = a * X3 ** 3 + b * X3 ** 2 + c * X3 + d

    return [[X1, dy1], [X2, dy2], [X3, dy3]]


if __name__ == '__main__':
    print(sheng_jin(-1, 2, 3, 4))
