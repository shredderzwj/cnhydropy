# -*- coding:utf-8 -*-
# 拓扑关系计算处理模块

import math
import random


def is_in_area(point, points):
    """
    判断一点是否位于指定封闭多边形内部
    :param point:  list [x, y] or tuple (x, y) -> 指定点坐标
    :param points:  [(x1, y1), (x2, y2), (x3, y3) ...] -> 多边形拐点坐标列表
    :return:  bool -> True 在内部； False 在外部； None 在边界上。
    """
    # 数据处理
    x, y = (float(point[0]), float(point[1]))
    ax, ay = list(zip(*points))

    # 如果给定点在多边形外边框以外，那么此点肯定不在多边形内部！
    if not (min(ax) <= x <= max(ax) and min(ay) <= y <= max(ay)):
        return False

    # 保证多边形的顶点不位于射线上
    while True:
        # 假定射线所在直线方程 ax + by + c = 0; (x, y) 为端点， (xp, yp)为方向
        xp = x + random.uniform(1, 100)
        yp = random.uniform(1, 100) * max(ay)
        # a, b, c 为假定射线所在的方程  参数
        a = yp - y
        b = x - xp
        c = xp * y - x * yp
        j = 0
        for i in range(len(ax)):
            if abs(a * ax[i] + b * ay[i] + c) < 1e-30:
                j += 1
        if j == 0:
            break
    # 判断射线与各个边的交点个数
    jd = 0
    for i in range(len(ax) - 1):
        tmpf1 = a * ax[i] + b * ay[i] + c
        tmpf2 = a * ax[i + 1] + b * ay[i + 1] + c
        tmpa = math.acos(
            ((ax[i] - x) * (xp - x) + (ay[i] - y) * (yp - y)) / math.sqrt(
                (ax[i] - x) ** 2 + (ay[i] - y) ** 2) / math.sqrt(
                (xp - x) ** 2 + (yp - y) ** 2))
        tmpb = math.acos(((ax[i + 1] - x) * (xp - x) + (ay[i + 1] - y) * (yp - y)) / math.sqrt(
            (ax[i + 1] - x) ** 2 + (ay[i + 1] - y) ** 2) / math.sqrt(
            (xp - x) ** 2 + (yp - y) ** 2))
        if (tmpf1 * tmpf2 < 0) and (tmpa + tmpb - math.pi < 0):
            jd += 1
        if tmpf1 * tmpf2 == 0:
            return None
    # 如果交点数为奇数，则位于内部；如果为偶数，位于外部。
    if math.fmod(jd, 2) == 0:
        return False
    else:
        return True


def quadrant8(point1, point2):
    """
    !将坐标系平均分为8个象限（逆时针方向编号为1-8）
    计算向量（x2-x1, y2-y1）位于哪个象限。
    :param point1: (x1, y1) 点坐标
    :param point2: (x2, y2) 点坐标
    :return: int 第几象限 1~8
    """
    x1, y1 = point1
    x2, y2 = point2
    a = x2 - x1
    b = y2 - y1
    if (a > 0) and (b >= 0):
        if a > b:
            return 1
        else:
            return 2
    elif (a <= 0) and (b > 0):
        if a < -b:
            return 3
        else:
            return 4
    elif (a < 0) and (b <= 0):
        if a < b:
            return 5
        else:
            return 6
    else:
        if a < -b:
            return 7
        else:
            return 8
