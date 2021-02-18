"""
查关系曲线图。
    根据矢量化的关系曲线散点[(x1, y1), (x2, y2), ...]，给定x0，计算y0
"""
import os
import json

from cnhydropy.utils.decorators import singleton

RESOURCE_DIR = os.path.dirname(os.path.abspath(__file__))


class RelationshipInterface(object):
    points = None

    def __init__(self):
        if self.points is None:
            raise NotImplementedError('未实现接口：%s；或实现接口时未设置必要参数' % self.__class__)
        points = sorted(self.points, key=lambda x: x[0])
        self.xs, self.ys = zip(*points)

    def linear_my(self, x: float):
        xs, ys = (self.xs, self.ys)
        if x in xs:
            return ys[xs.index(x)]
        if x < xs[0]:
            return ys[0]
        if x > xs[-1]:
            return ys[-1]
        for i, x_in_xs in enumerate(xs[:-1]):
            if x_in_xs < x < xs[i + 1]:
                x1 = x_in_xs
                x2 = xs[i + 1]
                y1 = ys[i]
                y2 = ys[i + 1]
                return (x - x1) * (y2 - y1) / (x2 - x1) + y1

    def __call__(self, x):
        return self.linear_my(x)


class Relationship(RelationshipInterface):
    """关系类"""
    def __init__(self, points):
        """
        :param points: 矢量化的关系曲线散点[(x1, y1), (x2, y2), ...]，给定x0，计算y0
        """
        self.points = points
        super().__init__()


class MultiTypeRelationshipBase(object):
    """适合分类的关系图基类"""
    @staticmethod
    def get_cls(type_name, resource_file_name, encoding='utf-8', **kwargs):
        with open(os.path.join(RESOURCE_DIR, resource_file_name),
                  encoding=encoding, **kwargs) as f:
            return singleton(
                # 包装单例注册器
                type(type_name, (RelationshipInterface,), dict(points=json.load(f)))
            )


@singleton
class Relationship84TFAlphaArea1(MultiTypeRelationshipBase):
    """水文分区1的各历时暴雨时面深关系图"""
    def __init__(self):
        self.r10min = self.get_cls('Relationship84TFAlphaArea1_10min', 't-F-alpha_area1_10min.json')()
        self.r1h = self.get_cls('Relationship84TFAlphaArea1_1h', 't-F-alpha_area1_1h.json')()
        self.r6h = self.get_cls('Relationship84TFAlphaArea1_6h', 't-F-alpha_area1_6h.json')()
        self.r24h = self.get_cls('Relationship84TFAlphaArea1_24h', 't-F-alpha_area1_24h.json')()
        self.r3d = self.get_cls('Relationship84TFAlphaArea1_3d', 't-F-alpha_area1_3d.json')()


@singleton
class RelationshipTFAlphaArea234(MultiTypeRelationshipBase):
    """水文分区2、3、4的各历时暴雨时面深关系图"""
    def __init__(self):
        self.r10min = self.get_cls('RelationshipTFAlphaArea234_10min', 't-F-alpha_area234_10min.json')()
        self.r1h = self.get_cls('RelationshipTFAlphaArea234_1h', 't-F-alpha_area234_1h.json')()
        self.r6h = self.get_cls('RelationshipTFAlphaArea234_6h', 't-F-alpha_area234_6h.json')()
        self.r24h = self.get_cls('RelationshipTFAlphaArea234_24h', 't-F-alpha_area234_24h.json')()
        self.r3d = self.get_cls('RelationshipTFAlphaArea234_3d', 't-F-alpha_area234_3d.json')()


@singleton
class RelationshipTFAlphaArea56(MultiTypeRelationshipBase):
    """水文分区5、6的各历时暴雨时面深关系图"""
    def __init__(self):
        self.r10min = self.get_cls('RelationshipTFAlphaArea56_10min', 't-F-alpha_area56_10min.json')()
        self.r1h = self.get_cls('RelationshipTFAlphaArea56_1h', 't-F-alpha_area56_1h.json')()
        self.r6h = self.get_cls('RelationshipTFAlphaArea56_6h', 't-F-alpha_area56_6h.json')()
        self.r24h = self.get_cls('RelationshipTFAlphaArea56_24h', 't-F-alpha_area56_24h.json')()
        self.r3d = self.get_cls('RelationshipTFAlphaArea56_3d', 't-F-alpha_area56_3d.json')()


@singleton
class RelationshipTFAlphaAreaPY(MultiTypeRelationshipBase):
    """水文分区平原区的各历时暴雨时面深关系图（73图集）"""
    def __init__(self):
        self.r10min = self.get_cls('RelationshipTFAlphaAreaPY_10min', 't-F-alpha_areaPY_10min.json')()
        self.r1h = self.get_cls('RelationshipTFAlphaAreaPY_1h', 't-F-alpha_areaPY_1h.json')()
        self.r6h = self.get_cls('RelationshipTFAlphaAreaPY_6h', 't-F-alpha_areaPY_6h.json')()
        self.r24h = self.get_cls('RelationshipTFAlphaAreaPY_24h', 't-F-alpha_areaPY_24h.json')()
        self.r3d = self.get_cls('RelationshipTFAlphaAreaPY_3d', 't-F-alpha_areaPY_3d.json')()


@singleton
class RelationshipPRHills(MultiTypeRelationshipBase):
    """山丘区降雨径流关系曲线图（84图集）"""
    def __init__(self):
        self.instances = {
            1: self.get_cls('RelationshipPRHills_1', 'P+Pa--R_area1.json')(),
            2: self.get_cls('RelationshipPRHills_2', 'P+Pa--R_area2.json')(),
            3: self.get_cls('RelationshipPRHills_3', 'P+Pa--R_area3.json')(),
            4: self.get_cls('RelationshipPRHills_4', 'P+Pa--R_area4.json')(),
            5: self.get_cls('RelationshipPRHills_5', 'P+Pa--R_area5.json')(),
            61: self.get_cls('RelationshipPRHills_61', 'P+Pa--R_area61.json')(),
            62: self.get_cls('RelationshipPRHills_62', 'P+Pa--R_area62.json')(),
            63: self.get_cls('RelationshipPRHills_63', 'P+Pa--R_area63.json')(),
        }
        self.areas = self.instances.keys()
        self._Imax = {1: 50, 2: 45, 3: 40, 4: 50, 5: 55, 61: 60, 62: 60, 63: 60}
        self._K = {1: 0.83, 2: 0.8, 3: 0.8, 4: 0.83, 5: 0.83, 61: 0.85, 62: 0.85, 63: 0.85}

    def __filter_area(self, obj, area):
        if area in self.areas:
            return obj.get(area)
        else:
            raise ValueError('输入区域代码错误！')

    def R(self, area: int, ppa: float):
        """
        河南省山区丘陵区降雨径流关系曲线图（84图集）
        :param area: int 曲线（区域）代码：
                    1：水文分区Ⅰ区。植被较好的淮南各支流浅山区。
                    2：水文分区Ⅱ区。植被较差的土石山区。
                    3：水文分区Ⅲ区大部分范围。植被较差、岩石裸露、土层瘠薄的山区
                    4：水文分区Ⅳ区。植被较好、有稀疏林木、野草茂密、土层稍厚的山区
                    5：水文分区Ⅴ区大部分范围。植被一般的土层较厚地区，如伊河嵩县、洛河长水以下的浅山区
                    61：水文分区Ⅵ区中的豫北山区和Ⅴ区中的伊洛涧河的黄土丘陵沟壑地区
                    62：豫北山区中喀斯特溶洞比较发育、并有河谷盆地的石灰岩地区。如小南海水库以上地区
                    63：蟒河瑞村以上地区
                    注：各分区中，如有流域下垫面情况与分区描述出入较大时，可以在和相邻分区内跨一区选用合适的线型
        :param ppa: float 平原区 P+Pa——本次降雨量+前期影响雨量（mm）
        :return: 径流深R
        """
        return self.__filter_area(self.instances, area)(ppa)

    def Imax(self, area):
        """
        :param area: int 曲线（区域）代码：
                    1：水文分区Ⅰ区。植被较好的淮南各支流浅山区。
                    2：水文分区Ⅱ区。植被较差的土石山区。
                    3：水文分区Ⅲ区大部分范围。植被较差、岩石裸露、土层瘠薄的山区
                    4：水文分区Ⅳ区。植被较好、有稀疏林木、野草茂密、土层稍厚的山区
                    5：水文分区Ⅴ区大部分范围。植被一般的土层较厚地区，如伊河嵩县、洛河长水以下的浅山区
                    61：水文分区Ⅵ区中的豫北山区和Ⅴ区中的伊洛涧河的黄土丘陵沟壑地区
                    62：豫北山区中喀斯特溶洞比较发育、并有河谷盆地的石灰岩地区。如小南海水库以上地区
                    63：蟒河瑞村以上地区
                    注：各分区中，如有流域下垫面情况与分区描述出入较大时，可以在和相邻分区内跨一区选用合适的线型
        :return: float
        """
        return self.__filter_area(self._Imax, area)

    def pa(self, area: int, p: float):
        """
        前期影响雨量
        :param area: int 曲线（区域）代码：
                    1：水文分区Ⅰ区。植被较好的淮南各支流浅山区。
                    2：水文分区Ⅱ区。植被较差的土石山区。
                    3：水文分区Ⅲ区大部分范围。植被较差、岩石裸露、土层瘠薄的山区
                    4：水文分区Ⅳ区。植被较好、有稀疏林木、野草茂密、土层稍厚的山区
                    5：水文分区Ⅴ区大部分范围。植被一般的土层较厚地区，如伊河嵩县、洛河长水以下的浅山区
                    61：水文分区Ⅵ区中的豫北山区和Ⅴ区中的伊洛涧河的黄土丘陵沟壑地区
                    62：豫北山区中喀斯特溶洞比较发育、并有河谷盆地的石灰岩地区。如小南海水库以上地区
                    63：蟒河瑞村以上地区
                    注：各分区中，如有流域下垫面情况与分区描述出入较大时，可以在和相邻分区内跨一区选用合适的线型
        :param p: 频率
        :return: float
        """
        return self.Imax(area) if p <= 1 / 50 else self.Imax(area) * 2 / 3

    def K(self, area):
        """
        :param area: int 曲线（区域）代码：
                    1：水文分区Ⅰ区。植被较好的淮南各支流浅山区。
                    2：水文分区Ⅱ区。植被较差的土石山区。
                    3：水文分区Ⅲ区大部分范围。植被较差、岩石裸露、土层瘠薄的山区
                    4：水文分区Ⅳ区。植被较好、有稀疏林木、野草茂密、土层稍厚的山区
                    5：水文分区Ⅴ区大部分范围。植被一般的土层较厚地区，如伊河嵩县、洛河长水以下的浅山区
                    61：水文分区Ⅵ区中的豫北山区和Ⅴ区中的伊洛涧河的黄土丘陵沟壑地区
                    62：豫北山区中喀斯特溶洞比较发育、并有河谷盆地的石灰岩地区。如小南海水库以上地区
                    63：蟒河瑞村以上地区
                    注：各分区中，如有流域下垫面情况与分区描述出入较大时，可以在和相邻分区内跨一区选用合适的线型
        :return: float
        """
        return self.__filter_area(self._K, area)


@singleton
class RelationshipPRFlat(MultiTypeRelationshipBase):
    """河南省平原地区降雨径流关系曲线图（73图集）"""
    def __init__(self):
        self.instances = {
            1: self.get_cls('RelationshipPRFlat_1', 'P+Pa--R_areaPY1.json')(),
            2: self.get_cls('RelationshipPRFlat_2', 'P+Pa--R_areaPY2.json')(),
            3: self.get_cls('RelationshipPRFlat_3', 'P+Pa--R_areaPY3.json')(),
            4: self.get_cls('RelationshipPRFlat_4', 'P+Pa--R_areaPY4.json')(),
            5: self.get_cls('RelationshipPRFlat_5', 'P+Pa--R_areaPY5.json')(),
            6: self.get_cls('RelationshipPRFlat_6', 'P+Pa--R_areaPY5.json')(),
            7: self.get_cls('RelationshipPRFlat_7', 'P+Pa--R_areaPY7.json')(),
            8: self.get_cls('RelationshipPRFlat_8', 'P+Pa--R_areaPY8.json')(),
        }
        self.areas = self.instances.keys()
        self._Imax = {1: 100, 2: 100, 3: 100, 4: 100, 5: 100, 6: 100, 7: 100, 8: 100}
        self._K = {1: 0.9, 2: 0.9, 3: .09, 4: 0.9, 5: 0.9, 6: 0.9, 7: 0.9, 8: 0.9}

    def __filter_area(self, obj, area):
        if area in self.areas:
            return obj.get(area)
        else:
            raise ValueError('输入区域代码错误！')

    def R(self, area: int, ppa: float):
        """
        河南省平原地区降雨径流关系曲线图（73图集）
        :param area: int 曲线（区域）代码：
                    1: 汝河、闾河
                    2: 洪河
                    3: 汾泉河、黑茨河
                    4: 浍河、包河、颍河
                    5: 沱河、王引河
                    6: 涡河、惠济河
                    7: 豫北
                    8: 沙土区
                    说明：各线型系综合代表线应用时可根据规划计所在地区的具体情况自然地理情况
                         对照选用线型或插补。
        :param ppa: float 平原区 P+Pa——本次降雨量+前期影响雨量（mm）
        :return: 径流深R
        """
        return self.__filter_area(self.instances, area)(ppa)

    def Imax(self, area):
        """
        :param area: int 曲线（区域）代码：
                    1: 汝河、闾河
                    2: 洪河
                    3: 汾泉河、黑茨河
                    4: 浍河、包河、颍河
                    5: 沱河、王引河
                    6: 涡河、惠济河
                    7: 豫北
                    8: 沙土区
                    说明：各线型系综合代表线应用时可根据规划计所在地区的具体情况自然地理情况
                         对照选用线型或插补。
        :return: float
        """
        return self.__filter_area(self._Imax, area)

    def K(self, area):
        """
        :param area: int 曲线（区域）代码：
                    1: 汝河、闾河
                    2: 洪河
                    3: 汾泉河、黑茨河
                    4: 浍河、包河、颍河
                    5: 沱河、王引河
                    6: 涡河、惠济河
                    7: 豫北
                    8: 沙土区
                    说明：各线型系综合代表线应用时可根据规划计所在地区的具体情况自然地理情况
                         对照选用线型或插补。
        :return: float
        """
        return self.__filter_area(self.K, area)

    def pa(self, area: int, p: float):
        """
        前期影响雨量
        :param area: int 曲线（区域）代码：
                    1: 汝河、闾河
                    2: 洪河
                    3: 汾泉河、黑茨河
                    4: 浍河、包河、颍河
                    5: 沱河、王引河
                    6: 涡河、惠济河
                    7: 豫北
                    8: 沙土区
                    说明：各线型系综合代表线应用时可根据规划计所在地区的具体情况自然地理情况
                         对照选用线型或插补。
        :param p: 频率
        :return: float
        """
        return self.Imax(area) if p <= 1 / 50 else self.Imax(area) * 2 / 3


@singleton
class RelationshipThetaM(MultiTypeRelationshipBase):
    """推理公式汇流参数地区综合θ~m关系图（84图集）"""
    def __init__(self):
        self.chart_instances = {
            1: self.get_cls('RelationshipThetaM_1', 'theta-m_area1.json')(),
            2: self.get_cls('RelationshipThetaM_2', 'theta-m_area2.json')(),
            3: self.get_cls('RelationshipThetaM_3', 'theta-m_area3.json')(),
            4: self.get_cls('RelationshipThetaM_4', 'theta-m_area4.json')(),
            5: self.get_cls('RelationshipThetaM_5', 'theta-m_area5.json')(),
            6: self.get_cls('RelationshipThetaM_6', 'theta-m_area5.json')(),
        }
        self.fit_funcs = {
            1: lambda theta: 0.314287 * theta ** 0.404842,
            2: lambda theta: 0.478361 * theta ** 0.400535,
            3: lambda theta: 0.575721 * theta ** 0.401817,
            4: lambda theta: 0.417826 * theta ** 0.400506,
            5: lambda theta: 0.511508 * theta ** 0.404065,
            6: lambda theta: 0.511508 * theta ** 0.404065,
        }
        self.areas = self.chart_instances.keys()

    @staticmethod
    def theta(F: float, L: float, J: float):
        return L / F**0.25 / J**(1/3)

    def m(self, area: int, theta: float, method: str = 'fit'):
        """
        计算推理公式汇流参数m
        :param area: int 84图集水文分区
        :param theta: float θ
        :param method: str
                    "fit"：使用拟合参数，默认值
                    "chart"：查关系图（线性插值）
        :return: float m 汇流参数
        """
        if area not in self.areas:
            raise ValueError('输入区域代码错误！')
        if method == 'chart':
            return self.chart_instances.get(area)(theta)
        else:
            return self.fit_funcs.get(area)(theta)


@singleton
class RelationshipAreaMu(object):
    """平均入渗率μ"""
    def __init__(self):
        self.mus = {1: 2, 2: 3, 3: 4, 4: 3, 5: 5, 6: 5}
        self.areas = self.mus.keys()

    def mu(self, area: int):
        """
        :param area: int 84图集水文分区
        :return: float 均入渗率μ
        """
        if area in self.areas:
            return self.mus.get(area)
        else:
            raise ValueError('输入区域代码错误！')

    def __call__(self, area: int):
        return self.mu(area)

    def __str__(self):
        result = '平均入渗率，以mm/h计，μ值分区数值表如下：\n'
        result += '水文分区:\t Ⅰ, \t Ⅱ Ⅳ,\t Ⅲ,\tⅤ Ⅵ\n'
        result += 'μ(mm/h):\t2~3,\t  3~5,\t4~6,\t 5~8'
        return result


if __name__ == '__main__':
    r = Relationship84TFAlphaArea1()
    print(r.r1h(200))

    r1 = RelationshipPRHills()
    r11 = RelationshipPRHills()
    print(r1, r11)
    print(r1.R(1, 300))

    r3 = RelationshipPRFlat()
    print(r3.R(1, 300))

    r3 = RelationshipThetaM()
    print(r3.m(1, 80))

    r4 = RelationshipThetaM()
    print(r4.m(1, 80, 'chart'))

    r5 = RelationshipAreaMu()
    print(r5.mu(1))
    print(r5)
