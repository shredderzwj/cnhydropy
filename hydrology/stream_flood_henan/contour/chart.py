"""
河南省中小流域设计暴雨洪水图集自动查图模块：
    Area84TJ 水文分区类，用于获取输入坐标点所在水文分区
    Contour..T.. 等值线类，用于查等值线给定坐标处的值（使用线性插值法）
"""
import os
from collections import defaultdict

import numpy as np
from scipy import interpolate
from pyproj import Proj

from ..topology import is_in_area
from ..register import singleton
from ..exception import CoordNotInHeNanError, TransformParamError
from . import geo

try:
    from . import transform_param as tp
except ModuleNotFoundError:
    raise ModuleNotFoundError(
        """
        等值线的矢量化，以及通过Proj转换经纬度坐标至矢量化后的平面坐标，
        本人进行了大量的实验研究，花费了大量的时间及精力，最终确定了合适的转换坐标系
        以及转换参数，使误差可以几乎达到小于等值线图上线宽的程度。这项内容不再无偿提供，
        已被打包压缩至文件 transform_param.zip 文件中，并进行了加密，使用的时候需要
        获取密码，直接将文件 transform_param.py 解压至本目录下即可。

        此项内容暂时不会公开，如果你特别感兴趣，可以联系本人。
        Email：shredderzwj@hotmail.com
        """
    )

RESOURCE_DIR = os.path.dirname(os.path.abspath(__file__))


class TransformerInterface(object):
    """将经纬度坐标转换为配准的平面坐标，转换器接口"""
    proj_str = None
    transform_param = None
    graph_name = None

    def __init__(self, proj_str=None, transform_param=None):
        # 必须实现此接口，并设置正确的转换参数
        if self.transform_param is None or self.graph_name is None \
                or self.proj_str is None:
            raise NotImplementedError('未实现接口：%s；或实现接口时未设置必要参数' % self.__class__)
        try:
            # proj投影参数
            self.proj_param = self.transform_param[0]
            # 尺度参数（缩放比例）
            self.k = self.transform_param[1]
            # 位置参数（x、y方向平移量）
            self.dxy = np.array(self.transform_param[2])
            self.proj = Proj(self.proj_str.format(*self.proj_param))
        except TypeError or IndexError:
            raise TransformParamError('转换参数有误！')

    def transform(self, lng: float, lat: float):
        """
        将经纬度坐标转换为配准的平面坐标
        :param lng: 经度
        :param lat: 纬度
        :return: numpy.array shape=(2,) 平面坐标
        """
        coord = np.array(self.proj(lng, lat))
        return (coord - self.dxy) / self.k

    def __call__(self, *args, **kwargs):
        return self.transform(*args, **kwargs)


class ContourInterface(TransformerInterface):
    """等值线接口"""
    geo_data = None

    def __init__(self):
        # 必须实现此接口，并设置正确的转换参数及数据类
        if self.geo_data is None:
            raise NotImplementedError('未实现接口：%s；或实现接口时未设置必要参数' % self.__class__)
        self.contour_interpolation = self.get_interpolation(self.geo_data)
        super(ContourInterface, self).__init__()

    @classmethod
    def get_interpolation(cls, geo_data, **kwargs):
        """读等值线数据文件，并返回插值对象"""
        x = geo_data.x
        y = geo_data.y
        z = geo_data.z
        return interpolate.LinearNDInterpolator(np.array([x, y]).T, z)

    def __call__(self, lng: float, lat: float):
        """对等值线图进行插值，获取指定坐标（经纬度坐标）处的值"""
        coord = super(ContourInterface, self).__call__(lng, lat)
        return float(self.contour_interpolation(*coord))


class Area84TJBase(TransformerInterface):
    """水文分区类"""
    graph_name = '河南省中小流域设计暴雨洪水图集(84图集) - 河南省山丘区水文分区图'
    proj_str = tp.Area84TJ.proj_str
    transform_param = tp.Area84TJ.transform_param
    geo_data = geo.HN84T01

    def __init__(self):
        # 必须实现此接口，并设置正确的转换参数
        if self.geo_data is None:
            raise NotImplementedError('未实现接口：%s；或实现接口时未设置必要参数' % self.__class__)
        self.area_info = self.get_area_info(self.geo_data)
        super().__init__()

    @classmethod
    def get_area_info(cls, geo_data, **kwargs):
        """读等值线数据文件，并返回插值对象"""
        x = geo_data.x
        y = geo_data.y
        z = geo_data.z
        area_info = defaultdict(list)
        for i, area in enumerate(z):
            if int(area) > 0:
                area_info[int(area)].append([x[i], y[i]])
        return area_info

    def get_area(self, x, y):
        """
        获取指定坐标点（平面坐标）所在的水文分区
        :param x: 平面坐标x轴
        :param y: 平面坐标y轴
        :return: int 所在分区。当输入坐标点不在河南省境内，返回 -1
        """
        for i in self.area_info.keys():
            if is_in_area([x, y], self.area_info[i]):
                return i
        raise CoordNotInHeNanError('输入的坐标不在河南省内！')

    def __call__(self, lng: float, lat: float):
        """
        获取指定坐标点（经纬度坐标）所在水文分区
        :param lng: 经度
        :param lat: 纬度
        :return: int 所在分区。当输入坐标点不在河南省境内，返回 -1
        """
        coord = self.transform(lng, lat)
        return self.get_area(*coord)


@singleton
class Area84TJ(Area84TJBase):
    pass


@singleton
class Contour84T02(ContourInterface):
    graph_name = '河南省中小流域设计暴雨洪水图集(84图集) - 河南省年最大10分钟点雨量均值图'
    proj_str = tp.Contour84T02.proj_str
    transform_param = tp.Contour84T02.transform_param
    geo_data = geo.HN84T02


@singleton
class Contour84T03(ContourInterface):
    graph_name = '河南省中小流域设计暴雨洪水图集(84图集) - 河南省年最大10分钟点雨量变差系数图'
    proj_str = tp.Contour84T03.proj_str
    transform_param = tp.Contour84T03.transform_param
    geo_data = geo.HN84T03


@singleton
class Contour84T05(ContourInterface):
    graph_name = '河南省中小流域设计暴雨洪水图集(84图集) - 河南省年最大1小时点雨量均值图'
    proj_str = tp.Contour84T05.proj_str
    transform_param = tp.Contour84T05.transform_param
    geo_data = geo.HN84T05


@singleton
class Contour84T06(ContourInterface):
    graph_name = '河南省中小流域设计暴雨洪水图集(84图集) - 河南省年最大1小时点雨量变差系数图'
    proj_str = tp.Contour84T06.proj_str
    transform_param = tp.Contour84T06.transform_param
    geo_data = geo.HN84T06


@singleton
class Contour84T08(ContourInterface):
    graph_name = '河南省中小流域设计暴雨洪水图集(84图集) - 河南省年最大6小时点雨量均值图'
    proj_str = tp.Contour84T08.proj_str
    transform_param = tp.Contour84T08.transform_param
    geo_data = geo.HN84T08


@singleton
class Contour84T09(ContourInterface):
    graph_name = '河南省中小流域设计暴雨洪水图集(84图集) - 河南省年最大6小时点雨量变差系数图'
    proj_str = tp.Contour84T09.proj_str
    transform_param = tp.Contour84T09.transform_param
    geo_data = geo.HN84T09


@singleton
class Contour84T11(ContourInterface):
    graph_name = '河南省中小流域设计暴雨洪水图集(84图集) - 河南省年最大24小时点雨量均值图'
    proj_str = tp.Contour84T11.proj_str
    transform_param = tp.Contour84T11.transform_param
    geo_data = geo.HN84T11


@singleton
class Contour84T12(ContourInterface):
    graph_name = '河南省中小流域设计暴雨洪水图集(84图集) - 河南省年最大24小时点雨量变差系数图'
    proj_str = tp.Contour84T12.proj_str
    transform_param = tp.Contour84T12.transform_param
    geo_data = geo.HN84T12


@singleton
class Contour84T21(ContourInterface):
    graph_name = '河南省中小流域设计暴雨洪水图集(84图集) - 河南省短历时暴雨递减指数n1(t<1小时)图'
    proj_str = tp.Contour84T21.proj_str
    transform_param = tp.Contour84T21.transform_param
    geo_data = geo.HN84T21


@singleton
class Contour84T22(ContourInterface):
    graph_name = '河南省中小流域设计暴雨洪水图集(84图集) - 河南省短历时暴雨递减指数n2(t=1~6小时)图'
    proj_str = tp.Contour84T22.proj_str
    transform_param = tp.Contour84T22.transform_param
    geo_data = geo.HN84T22


@singleton
class Contour84T23(ContourInterface):
    graph_name = '河南省中小流域设计暴雨洪水图集(84图集) - 河南省短历时暴雨递减指数n3(t=6~24小时)图'
    proj_str = tp.Contour84T23.proj_str
    transform_param = tp.Contour84T23.transform_param
    geo_data = geo.HN84T23

