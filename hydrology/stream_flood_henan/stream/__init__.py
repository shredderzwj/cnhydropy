"""
设计暴雨查算
"""
import math
from collections import defaultdict

from cnhydropy.hydrology.stream_flood_henan import contour
from cnhydropy.hydrology.stream_flood_henan import relationship
from cnhydropy.hydrology.frequency_analysis import PearsonThree


class Stream(object):
    """流域暴雨参数"""

    def __init__(self, lng: float, lat: float):
        """
        :param lng: float 流域重心处的经度
        :param lat: float 流域重心处的纬度
        """
        self.lng = lng
        self.lat = lat
        self.area = contour.Area84TJ()(lng, lat)
        """最大10分钟点雨量均值"""
        self.h_10min = contour.Contour84T02()(self.lng, self.lat)
        """最大10分钟点雨量变差系数"""
        self.cv_10min = contour.Contour84T03()(self.lng, self.lat)
        self.h_1h = contour.Contour84T05()(self.lng, self.lat)
        self.cv_1h = contour.Contour84T06()(self.lng, self.lat)
        self.h_6h = contour.Contour84T08()(self.lng, self.lat)
        self.cv_6h = contour.Contour84T09()(self.lng, self.lat)
        self.h_24h = contour.Contour84T11()(self.lng, self.lat)
        self.cv_24h = contour.Contour84T12()(self.lng, self.lat)
        self.n1 = contour.Contour84T21()(self.lng, self.lat)
        self.n2 = contour.Contour84T22()(self.lng, self.lat)
        self.n3 = contour.Contour84T23()(self.lng, self.lat)

    def show_param(self):
        print('\n'.join(self.__str__().split('\n')[1:]))

    def __str__(self):
        s = str(super().__str__())
        s += '\n流域重心处坐标为：(%.6f, %.6f)\n' % (self.lng, self.lat)
        s += '所在水文分区为：%d\n' % self.area
        s += '流域暴雨参数：\n'
        s += '\t最大10分钟点雨量均值：%.3f\n' % self.h_10min
        s += '\t最大10分钟点雨量变差系数：%.3f\n' % self.cv_10min
        s += '\t最大1小时点雨量均值：%.3f\n' % self.h_1h
        s += '\t最大1小时点雨量变差系数：%.3f\n' % self.cv_1h
        s += '\t最大6小时点雨量均值：%.3f\n' % self.h_6h
        s += '\t最大6小时点雨量变差系数：%.3f\n' % self.cv_6h
        s += '\t最大24小时点雨量均值：%.3f\n' % self.h_24h
        s += '\t最大24小时点雨量变差系数：%.3f\n' % self.cv_24h
        s += '\t短历时暴雨递减指数n1(t<1小时)：%.3f\n' % self.n1
        s += '\t短历时暴雨递减指数n2(t=1~6小时)：%.3f\n' % self.n2
        s += '\t短历时暴雨递减指数n3(t=6~24小时)：%.3f\n' % self.n3
        return s


class DesignStream(object):
    _alpha_10min = None
    _alpha_1h = None
    _alpha_6h = None
    _alpha_24h = None
    _alpha_3d = None

    def __init__(self, stream: Stream, f: float, p: float,
                 ratio: float = 3.5, project_type: int = 1):
        """
        :param stream: Stream 暴雨参数对象
        :param f: float 集雨面积，平方公里
        :param p: float 设计频率，注意，此参数非百分比。
        :param project_type: int 工程类型
        :param ratio: float Cs/Cv值。
                1：中小水库（计算希遇频率洪水，考虑不同时段雨量变差系数Cv及暴雨点面关系）
                2：小型农水（计算常用频率洪水，不考虑频率的变化及暴雨点面关系的影响，概化计算，不建议采用）
        """
        self.stream = stream
        self.lng, self.lat = (stream.lng, stream.lat)
        self.__area = stream.area
        self.f = f
        self.__p = self.__check_p(p)
        self.ratio = ratio
        self.project_type = project_type
        self.mu = relationship.RelationshipAreaMu()(self.__area)
        # 以下4个为计算各历时暴雨参数相应的模比系数函数
        self.get_kp_10min = PearsonThree(self.stream.cv_10min, self.stream.cv_10min * ratio).calc_kp
        self.get_kp_1h = PearsonThree(self.stream.cv_1h, self.stream.cv_1h * ratio).calc_kp
        self.get_kp_6h = PearsonThree(self.stream.cv_6h, self.stream.cv_6h * ratio).calc_kp
        self.get_kp_24h = PearsonThree(self.stream.cv_24h, self.stream.cv_24h * ratio).calc_kp
        # 点面折减系数初始化
        self.__init_alpha(f)

    def show_param(self):
        print('\n'.join(self.__str__().split('\n')[1:]))

    def __str__(self):
        s = str(super().__str__())
        s += '\n设计频率为：%.2f%%\n' % (self.p*100)
        s += '暴雨递减指数n1：%.3f\n' % self.n1
        s += '暴雨递减指数n2：%.3f\n' % self.n2
        s += '暴雨递减指数n3：%.3f\n' % self.n3
        s += '设计频率下最大10分钟点雨量：%.2f\n' % self.design_h_10min
        s += '设计频率下最大1小时点雨量：%.2f\n' % self.design_h_1h
        s += '设计频率下最大6小时点雨量：%.2f\n' % self.design_h_6h
        s += '设计频率下最大24小时点雨量：%.2f\n' % self.design_h_24h
        s += '历时10分钟暴雨点面折减系数：%.2f\n' % self.alpha_10min
        s += '历时1小时暴雨点面折减系数：%.2f\n' % self.alpha_1h
        s += '历时6小时暴雨点面折减系数：%.2f\n' % self._alpha_6h
        s += '历时24小时暴雨点面折减系数：%.2f\n' % self._alpha_24h
        s += '设计频率下最大10分钟面雨量：%.2f\n' % self.design_hf_10min
        s += '设计频率下最大1小时面雨量：%.2f\n' % self.design_hf_1h
        s += '设计频率下最大6小时面雨量：%.2f\n' % self.design_hf_6h
        s += '设计频率下最大24小时面雨量：%.2f\n' % self.design_hf_24h
        # s += '历时3天暴雨点面折减系数：%.2f\n' % self.alpha_3d
        s += '设计24小时暴雨时程分配（设计静雨过程）：\n'
        for (t, v) in self.design_rain_type_24h:
            s += '\t%d\t%.2f\n' % (int(t), float(v))
        s += '平均入渗强度μ：%.2f\n' % self.mu
        s += '逐时净雨：\n'
        for (t, v) in self.hourly_net_rain():
            s += '\t%d\t%.2f\n' % (int(t), float(v))
        return s

    @property
    def p(self):
        return self.__p

    @p.setter
    def p(self, p):
        self.__p = self.__check_p(p)

    @property
    def area(self):
        return self.__area

    @area.setter
    def area(self, area):
        self.__area = area
        self.__init_alpha(self.f)

    @staticmethod
    def __check_p(p):
        """检查涉及频率值的合理性"""
        try:
            p = float(p)
        except ValueError:
            raise ValueError('输入的设计频率值有误：{}'.format(p))
        if not (0 < p < 1):
            raise ValueError('设计频率值取值范围应为：(0, 1)')
        return p

    def __init_alpha(self, f):
        """点面折减系数"""
        if self.area == 1:
            r = relationship.Relationship84TFAlphaArea1()
        elif self.area in [2, 3, 4]:
            r = relationship.RelationshipTFAlphaArea234()
        elif self.area in [5, 6]:
            r = relationship.RelationshipTFAlphaArea56()
        else:
            r = relationship.RelationshipTFAlphaAreaPY()
        self._alpha_10min = r.r10min(f)
        self._alpha_1h = r.r1h(f)
        self._alpha_6h = r.r6h(f)
        self._alpha_24h = r.r24h(f)
        self._alpha_3d = r.r3d(f)

    @property
    def alpha_10min(self):
        """10分钟点面折减系数"""
        return self._alpha_10min

    @property
    def alpha_1h(self):
        """1h点面折减系数"""
        return self._alpha_1h

    @property
    def alpha_6h(self):
        """6h点面折减系数"""
        return self._alpha_6h

    @property
    def alpha_24h(self):
        """24h点面折减系数"""
        return self._alpha_24h

    @property
    def alpha_3d(self):
        """3d点面折减系数"""
        return self._alpha_3d

    @property
    def n1(self):
        """暴雨递减指数n1"""
        if self.project_type == 2:
            return self.stream.n1
        return 1 - 1.285 * math.log10(
            self.alpha_1h * self.design_h_1h /
            self.alpha_10min / self.design_h_10min
        )

    @property
    def n2(self):
        """暴雨递减指数n2"""
        if self.project_type == 2:
            return self.stream.n2
        return 1 - 1.285 * math.log10(
            self.alpha_6h * self.design_h_6h /
            self.alpha_1h / self.design_h_1h
        )

    @property
    def n3(self):
        """暴雨递减指数n3"""
        if self.project_type == 2:
            return self.stream.n3
        return 1 - 1.661 * math.log10(
            self.alpha_24h * self.design_h_24h /
            self.alpha_6h / self.design_h_6h
        )

    @property
    def design_h_10min(self):
        """设计10分钟点雨量"""
        return self.get_kp_10min(self.p) * self.stream.h_10min

    @property
    def design_h_1h(self):
        """设计1小时点雨量"""
        return self.get_kp_1h(self.p) * self.stream.h_1h

    @property
    def design_h_6h(self):
        """设计6小时点雨量"""
        return self.get_kp_6h(self.p) * self.stream.h_6h

    @property
    def design_h_24h(self):
        """设计24小时点雨量"""
        return self.get_kp_24h(self.p) * self.stream.h_24h

    def design_ht(self, t: float):
        """
        其他不同历时的设计点雨量计算
        :param t: float 历时
        :return: float
        """
        eps = 1e-8
        if math.fabs(t - 1 / 6) < eps:
            return self.design_h_10min
        elif math.fabs(t - 1) < eps:
            return self.design_h_1h
        elif math.fabs(t - 6) < eps:
            return self.design_h_6h
        elif math.fabs(t - 24) < eps:
            return self.design_h_24h
        elif t < 1:
            return self.design_h_1h * t ** (1 - self.n1)
        elif 1 < t < 6:
            return self.design_h_1h * t ** (1 - self.n2)
        elif 6 < t < 24:
            return self.design_h_24h * 24 ** (self.n3 - 1) * t ** (1 - self.n3)
        else:
            raise ValueError('暴雨历时取值范围应为(0, 24]')

    @property
    def design_hf_10min(self):
        """设计10分钟面雨量"""
        return self.design_h_10min * self.alpha_10min

    @property
    def design_hf_1h(self):
        """设计1小时面雨量"""
        return self.design_h_1h * self.alpha_1h

    @property
    def design_hf_6h(self):
        """设计6小时面雨量"""
        return self.design_h_6h * self.alpha_6h

    @property
    def design_hf_24h(self):
        """设计24小时面雨量"""
        return self.design_h_24h * self.alpha_24h

    def design_hft(self, t: float):
        """
        其他不同历时的设计面雨量计算
        :param t: float 历时
        :return: float
        """
        eps = 1e-8
        if math.fabs(t - 1 / 6) < eps:
            return self.design_hf_10min
        elif math.fabs(t - 1) < eps:
            return self.design_hf_1h
        elif math.fabs(t - 6) < eps:
            return self.design_hf_6h
        elif math.fabs(t - 24) < eps:
            return self.design_hf_24h
        elif t < 1:
            return self.design_hf_1h * t ** (1 - self.n1)
        elif 1 < t < 6:
            return self.design_hf_1h * t ** (1 - self.n2)
        elif 6 < t < 24:
            return self.design_hf_24h * 24 ** (self.n3 - 1) * t ** (1 - self.n3)
        else:
            raise ValueError('暴雨历时取值范围应为(0, 24]')

    @property
    def design_rain_type_24h(self):
        """
        设计24小时暴雨时程分配（设计降雨过程）
        :return: list 1~24小时的暴雨时程分配,数据结构为 [(1, r1), (2, r2), ……(24, r24)]
        """
        hft = defaultdict(float)
        design_hft = defaultdict(float)
        for t in range(1, 25):
            hft[t] = self.design_hft(t)

        for t in range(1, 7):
            design_hft[t] = (1 / 6 * (hft[24] - hft[18]))

        for i, t in enumerate(range(7, 15)):
            design_hft[t] = (hft[23-t-i] - hft[22-t-i])

        for i, t in enumerate(range(16, 24)):
            design_hft[t] = (hft[t-13+i] - hft[t-14+i])

        design_hft[15] = hft[1]
        design_hft[24] = (hft[18] - hft[17])
        return sorted(list(design_hft.items()), key=lambda x: x[0])

    def hourly_net_rain(self, mu: float = None):
        """
        逐时净雨
        :param mu: 平均入渗率，以mm/h计
        :return: list 1~24小时的逐时净雨，数据结构为 [(1, r1), (2, r2), ……(24, r24)]
        """
        if mu is None:
            mu = self.mu
        return [(t, max(0, v - mu)) for (t, v) in self.design_rain_type_24h]


if __name__ == '__main__':
    """输入流域特征属性，计算暴雨参数"""
    F = 72  # 流域面积
    L = 18  # 河道长度
    J = 0.0035  # 河道平均比降
    coord = (113, 34)  # 流域重心坐标
    stream = Stream(*coord)  # 暴雨参数对象（只与流域特征相关，也就是查图集得到的参数）

    """指定设计频率，计算设计暴雨参数"""
    p = 1 / 50  # 设计频率
    design_stream = DesignStream(stream, F, p, project_type=1)  # 设计暴雨参数对象

    print('-' * 20, '暴雨参数(查图结果)', '-' * 20)
    stream.show_param()
    print('\n')

    print('-' * 20, '设计暴雨', '-' * 20)
    design_stream.show_param()
    print('\n')

