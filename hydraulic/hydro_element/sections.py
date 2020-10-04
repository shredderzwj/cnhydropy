# -*- coding:utf-8 -*-
# 水力相关计算模块

import math


class SectionElement(object):
	"""
	断面水利要素类，
	根据过水断面几何形式计算过水面积，湿周，水力半径等水力要素
	根据传入参数不同自动判断是哪种形式的断面，分为以下三种：
		1、实测地形河道断面，已知断面实测的各拐点坐标
		2、标准梯形断面，已知底宽、边坡坡度（矩形断面为0）
		3、U型断面，圆弧半径r，圆弧圆心角theta，直线段倾斜角alpha（与竖直方向夹角）
			（参考：https://wenku.baidu.com/view/e6b737b3524de518964b7dbb.html?rec_flag=default&sxts=1560401355713）
	"""
	def __init__(self, coords_or_a_or_r, m_or_theta=None, alpha=None):
		"""
		初始化参数
		:param coords_or_a_or_r:  位置参数1，
			如果是天然实测断面，为列表或元组 [(x1, y1), (x2, y2) ...]
			如果是梯形（矩形）断面， 此参数为 float， 底宽 a
			如果是U型断面， 此参数为 float， 圆弧半径 r
		:param m_or_theta: 位置参数2，
			如果是天然实测断面，无此参数
			如果是梯形（矩形）断面， 此参数为 float， 边坡系数 m
			如果是U型断面， 此参数为 float， 圆弧圆心角（劣弧） theta （单位：度）
		:param alpha: 位置参数3，
			如果是天然实测断面，无此参数
			如果是梯形（矩形）断面， 无此参数
			如果是U型断面， 此参数为 float， 直线段的倾斜角（与竖直方向夹角） alpha （单位：度）
		"""
		if isinstance(coords_or_a_or_r, list) or isinstance(coords_or_a_or_r, tuple):
			self.type = 'nature'
			self.coords = coords_or_a_or_r
		else:
			if alpha is None:
				self.type = 'trapezium'
				self.a = coords_or_a_or_r
				self.m = m_or_theta
			else:
				self.type = 'U'
				self.r = coords_or_a_or_r
				self.theta = m_or_theta
				self.alpha = alpha
				self.h1 = self.r * (1 - math.cos(self.theta * math.pi / 180 / 2))    # 圆弧段高度
	
	def __calc_element_nature__(self, h):
		"""
		计算 过水面积，湿周，水力半径等水力要素
		:param h: float 水位
		:return: dict {'A': 过水面积, 'X': 湿周, 'R':水力半径}
		"""
		x, y = list(zip(*self.coords))
		if h < min(y):
			print('水位低于河底！')
			raise ValueError
		if h > max(y):
			print('水位高于堤顶！')
			raise ValueError
		# 排序
		for i in range(0, len(x) - 1, 1):
			for j in range(i + 1, len(x), 1):
				if (x[i] > x[j]):
					tmpx = x[i]
					tmpy = y[i]
					x[i] = x[j]
					y[i] = y[j]
					x[j] = tmpx
					y[j] = tmpy
		# 计算 过水面积s，湿周ka
		s = 0
		ka = 0
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
			if (h <= y[i] and h > y[i + 1]) or (h < y[i] and h >= y[i + 1]):
				s = s + s1
				ka = ka + ka1
			elif (h >= y[i] and h < y[i + 1]) or (h > y[i] and h <= y[i + 1]):
				s = s + s2
				ka = ka + ka2
			elif h > y[i] and h > y[i + 1]:
				s = s + s3
				ka = ka + ka3
		# 计算水力半径r
		if ka == 0:
			s = 0
			r = 0
		else:
			r = s / ka
		return {'H': h - min(y), "A": s, 'X': ka, 'R': r}
	
	def __calc_element_trapezium__(self, h):
		"""
		计算 过水面积，湿周，水力半径等水力要素
		:param h: float 水深
		:return: dict {'H': 水深, 'A': 过水面积, 'X': 湿周, 'R':水力半径}
		"""
		if h <= 0:
			print('水深必须大于0!')
			raise ValueError
		a = self.a
		m = self.m
		s = h * (a + m * h)
		ka = 2 * h * math.sqrt(1 + m * m) + a
		r = s / ka
		return {'H': h, "A": s, 'X': ka, 'R': r}
		
	def __calc_element_U__(self, h):
		"""
		计算 过水面积，湿周，水力半径等水力要素
		:param h: float 水深
		:return: dict {'H': 水深, 'A': 过水面积, 'X': 湿周, 'R':水力半径}
		"""
		if h <= 0:
			print('水深必须大于0!')
			raise ValueError
		
		r = self.r
		theta = self.theta * math.pi / 180
		alpha = self.alpha * math.pi / 180
		h1 = self.h1
		
		if h <= h1:
			thetap = math.acos((r - h) / r) * 2
			ka = r * thetap
			s = thetap * r ** 2 / 2 - r * math.sin(thetap / 2) * (r - h)
			rr = s / ka
		else:
			h2 = h - h1
			ka = 2 * h2 / math.cos(alpha) + theta * r
			s = (theta * r ** 2 / 2 - r * math.sin(theta / 2) * (r - h1)) + (2 * r * math.sin(theta / 2) + h2 * math.tan(alpha)) * h2
			rr = s / ka
		return {'H': h, "A": s, 'X': ka, 'R': rr}

	def calc_element(self, h):
		"""
		计算 过水面积，湿周，水力半径等水力要素
		:param h: float 水深（水位）
		:return: dict {'A': 过水面积, 'X': 湿周, 'R':水力半径}
		"""
		if self.type == 'nature':
			element = self.__calc_element_nature__(h)
		elif self.type == 'trapezium':
			element = self.__calc_element_trapezium__(h)
		else:
			element = self.__calc_element_U__(h)
		return element
	
	def calc_Manning(self, h,  n, j):
		"""
		曼宁公式
		:param h: float 水深（水位）
		:param n: float 糙率
		:param j: float 比降
		:return: {"C": 谢才系数, 'Q': 设计流量, 'V': 平均流速}
		"""
		element = self.calc_element(h)
		R = element.get("R")
		A = element.get("A")
		C = 1 / n * R ** (1 / 6)
		V = C * math.sqrt(R * j)
		Q = A * V
		return {
			** element,
			"C": C,
			"V": V,
			"Q": Q,
		}


if __name__ == '__main__':
	coords = [
		(0.0661, 2.6351),
		(0.8979, 2.3418),
		(1.5829, 2.2196),
		(2.1448, 2.0000),
		(2.7817, 1.8531),
		(4.2008, 1.4123),
		(4.8125, 1.2168),
		(5.3996, 1.0702),
		(5.7185, 0.8999),
		(6.3048, 0.9235),
		(6.9654, 0.5570),
		(7.3568, 0.3370),
		(7.9195, 0.3370),
		(8.5311, 0.2882),
		(9.5095, 0.2646),
		(10.8062, 0.1180),
		(11.5646, 0.0691),
		(12.3721, 0.1904),
		(13.3752, 0.5814),
		(14.1825, 0.8013),
		(15.0143, 1.1679),
		(16.3844, 1.2657),
		(17.1917, 1.6322),
		(18.0478, 1.8531),
		(18.3658, 2.0974),
		(18.9040, 2.0974),
		(19.1976, 2.3418),
		(20.0000, 2.4736),
	]
	section1 = SectionElement(coords)
	print(section1.calc_Manning(2, 0.035, 0.001), '\n')
	
	section2 = SectionElement(3, 1.5)
	print(section2.calc_Manning(1.2, 0.035, 0.001), '\n')
	
	section3 = SectionElement(0.65, 151.933, 8)
	print(section3.calc_Manning(0.7, 0.035, 0.001))
