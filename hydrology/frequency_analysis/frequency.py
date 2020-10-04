# -*- coding: utf-8 -*-
# 水文相关计算包

import re
import numpy as np
import scipy.special
import scipy.stats
import scipy.optimize
from scipy import interpolate
from operator import itemgetter
import matplotlib.pyplot as plt

# plt.switch_backend('agg')  # 切换 matplotlib 绘图后端为agg。

# 设置 matplotlib 字体，解决中文乱码的问题（linux平台需要安装 SimHei 字体，macOS没用过）
plt.rcParams['font.family'] = ['sans-serif']
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


class PearsonThree(object):
    """
    P-III 曲线类，实际为一个gamma分布
        gamma分布参考文档：https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.gamma.html
    """
    colors = ['#ff0000', '#00ff00', '#0000ff', '#00ffff', '#ff00ff', '#ffff00']
    norm = scipy.stats.norm()

    def __init__(self, cv, cs, avg=1):
        """
        :param cv: float 变差系数
        :param cs: float 偏态系数
        :param avg: float 均值（若单纯计算模比系数Kp，此项可不指定）
        """
        self.__ticks = [
            '.01', '.02', '.05', '0.1', '0.2', '0.5', '1', '2', '5', '10', '20', '30', '40', '50', '60', '70',
            '80', '90', '95', '98', '99', '99.7', '99.9', '99.97', '99.99'
        ]
        self.ticks_array = np.array([float(x) for x in self.__ticks]) / 100
        self.__param = [cv, cs, avg]
        self.distribution = self.get_distribution(*self.__param)
        self.__heisen_coord_mapping_param()

    @property
    def param(self):
        return self.__param

    @param.setter
    def param(self, param):
        """
        设置设计参数
        :param param: list [Cv, Cs, 均值]
        """
        self.distribution = self.get_distribution(*param)
        self.__param = param

    @property
    def ticks(self):
        return self.__ticks

    @ticks.setter
    def ticks(self, ticks):
        """设置绘图频率轴的刻度（默认值是经过优化的，一般情况下不建议重新设置）"""
        self.ticks_array = np.array([float(x) for x in ticks]) / 100
        self.__ticks = ticks
        self.__heisen_coord_mapping_param()

    def __heisen_coord_mapping_param(self):
        self.U = self.norm.ppf(min(self.ticks_array))
        self.xs = self.norm.ppf(self.ticks_array) - self.U

    def __draw_curve_param(self):
        """获取绘图的 x, y 坐标值系列（插值）"""
        qs = self.calc_q(self.ticks_array)
        x = np.linspace(min(self.xs), max(self.xs), 100)
        func = interpolate.interp1d(self.xs, qs, kind='cubic')
        return x, func(x)

    @staticmethod
    def get_distribution(cv, cs, avg):
        """获取gamma分布对象"""
        shape = 4 / cs ** 2
        scale = avg * cv * cs / 2
        loc = avg * (1 - 2 * cv / cs)
        return scipy.stats.gamma(shape, loc, scale)

    def calc_q(self, p):
        """计算设计频率下的流量"""
        return self.distribution.isf(p)

    def calc_kp(self, p):
        """计算设计频率下的模比系数"""
        return self.distribution.isf(p) / self.param[-1]

    def create_figure(self, figsize=(15.3, 9.2), title='P-III曲线'):
        """创建绘制曲线的figure对象"""
        if hasattr(self, 'fig'):
            return self.fig
        self.fig = plt.figure(title, figsize=figsize)
        plt.title(title, {"size": 16})
        plt.xlabel('频率（%）', {'size': 14})
        plt.ylabel('流量（$m^3/s$）', {'size': 14})
        plt.grid(linestyle='--', linewidth=1, zorder=1)
        plt.xticks(self.xs, self.ticks)
        return self.fig

    def draw_curve(self, color=None, linewidth=2.0, alpha=1.0):
        """
        绘制拟合的曲线
        :param color: str 曲线颜色
        :param linewidth: float 线宽
        :param alpha: float 透明度，取值范围为[0,1]，0位完全透明，1为完全不透明
        :return: matplotlib.pyplot.figure 绘图对象
        """
        if color is None:
            color = self.colors[0]
        fig = self.create_figure()
        x, y = self.__draw_curve_param()
        plt.plot(
            x, y, label="\nCv=%.3f  Cs=%.3f  Qa=%.2f$m^3/s$\n" % tuple(self.param),
            color=color, linewidth=linewidth, alpha=alpha, zorder=2
        )
        plt.legend(prop={'size': 12}, framealpha=1)
        return fig

    def show(self):
        """显示绘图"""
        if not hasattr(self, 'fig'):
            self.draw_curve()
        plt.show()
        plt.cla()
        plt.close()
        delattr(self, 'fig')

    def save(self, path, format='png', figsize=(15.3, 9.2), dpi=96):
        """
        将图保存至文件
        :param path: 文件保存路径。
        :param format: str 图片文件格式， 详细支持格式见 matplotlib 文档
        :param figsize: tuple 设置保存图片尺寸
        :param dpi: int 设置保存图片的dpi
        :param args:
        :param kwargs:
        """
        if hasattr(self, 'fig'):
            plt.cla()
            plt.close()
            delattr(self, 'fig')
        self.create_figure(figsize=figsize)
        self.draw_curve()
        self.fig.set_size_inches(*figsize)
        self.fig.savefig(path, format=format, dpi=dpi, bbox_inches='tight')  # transparent=True)
        plt.cla()
        plt.close()
        delattr(self, 'fig')


class PearsonThreeContinuousFit(PearsonThree):
    """水文频率计算(连续系列),由于继承自P-III 曲线类，可以进行P-III 曲线相关计算"""
    acceptable_methods = ['moment', 'fit1', 'fit2', 'fit3', 'manual']

    def __init__(self, floods, methods='moment', is_fit_avg=True):
        """
        :param floods: list n*2 array like [(年份int, 洪水流量float), ……]
        :param method: str or list 估计参数的方法
                            "moment"->直接使用矩法；
                            "fit1"->适线法_离差平方和准则，采用矩法初步估计，然后适线(默认)；
                            "fit2"->适线法_离差绝对值和准则，采用矩法初步估计，然后适线；
                            "fit3"->适线法_相对离差平方和准则，采用矩法初步估计，然后适线。
                            "all" -> 以上所有方法对比
        :param is_fit_avg: bool 适线时是否对均值进行寻优。True表示对均值寻优(默认)，False表示采用矩法计算的均值。
                            在 method设置为非"moment"时生效。
        """

        self.floods = sorted(floods, key=itemgetter(1), reverse=True)
        self.__methods = self._checked_methods(methods)
        self.__is_fit_avg = is_fit_avg
        self.__pms = self._calc_pms()
        self.__param_moment = self._calc_param_moment()
        super().__init__(*self.__param_moment)  # 初始化设计参数为矩法计算的参数
        self.__params = self._calc_params()

    @property
    def methods(self):
        return self.__methods

    @methods.setter
    def methods(self, methods):
        self.__methods = self._checked_methods(methods)
        self.__params = self._calc_params()

    @property
    def is_fit_avg(self):
        return self.__methods

    @is_fit_avg.setter
    def is_fit_avg(self, is_fit_avg):
        self.__is_fit_avg = is_fit_avg
        self.__params = self._calc_params()

    @property
    def param_moment(self):
        return self.__param_moment

    @property
    def pms(self):
        return self.__pms

    @property
    def params(self):
        return self.__params

    @staticmethod
    def handle_floods_from_excel(data):
        """
        处理从Excel表格中（或者其他文件）复制过来的数据，使之符合PearsonThreeContinuousFit初始化参数输入的floods值的格式
        :param data: str 复制的数据。数据要求：
                         (1)第一列为年份，第二列为洪水流量值，
                         (2)中间以【空格、逗号、制表符、冒号、分号、星号、at符号、感叹号、竖线、斜杠线、井号】等分隔，
                         (3)每行一组数据。
        :return: list [(年份int, 洪水流量float), ……]
        """
        ret = []
        for x in data.strip().split('\n'):
            cell = re.sub(r'[\s,|:*/&%#@!;，。]+', ',', x.strip()).split(',')
            ret.append((int(cell[0]), float(cell[1])))
        return ret

    def _checked_methods(self, ms):
        if isinstance(ms, list or tuple):
            methods = [x for x in ms if x in self.acceptable_methods]
        else:
            methods = [ms] if ms in self.acceptable_methods else []
        if ms == 'all':
            methods = self.acceptable_methods[:-1]
        if not methods:
            raise ValueError('输入的 methods 参数有误！')
        return methods

    def _calc_pms(self):
        """
        计算经验频率
        :return: list [(年份1, 流量1, 频率1), (年份2, 流量2, 频率2), ……]
        """
        n = len(self.floods)
        return [(year, q, (i + 1) / (n + 1)) for i, (year, q) in enumerate(self.floods)]

    def _calc_param_moment(self):
        """
        矩法计算统计参数
        :return: list [Cv, Cs, 均值]
        """
        n = len(self.floods)
        years, qs = zip(*[(x, y) for x, y in self.floods])
        qa = np.average(qs)
        s = np.sqrt(1 / (n - 1) * np.sum([(q - qa) ** 2 for q in qs]))
        cv = s / qa
        cs = n * np.sum([(q - qa) ** 3 for q in qs]) / ((n - 1) * (n - 2) * qa ** 3 * cv ** 3)
        return [cv, cs, qa]

    def __optimize_goal_fit(self, p, qs, pms, avg, method):
        """适线寻优的目标函数"""
        if method == 'fit2':
            # 离差绝对值和准则
            return np.sqrt(np.abs(self.__optimize_func(p, pms, avg) - qs))
        elif method == 'fit3':
            # 相对离差平方和准则
            return (self.__optimize_func(p, pms, avg) - qs) / qs
        else:
            # 离差平方和准则
            return self.__optimize_func(p, pms, avg) - qs

    def __optimize_func(self, p, pms, avg):
        """根据优选的参数预测流量"""
        if self.is_fit_avg:
            cv, cs, avg_fit = p
            return PearsonThree(cv, cs, avg_fit).calc_q(np.array(pms))
        else:
            cv, cs = p
            return PearsonThree(cv, cs, avg).calc_q(np.array(pms))

    def _calc_params(self):
        """
        使用矩法进行参数估计初值,然后用指定的准则优化拟合配线， 如果找不到最优解，将使用矩法估计的值
        :return: dict {'method': [Cv, Cs, 均值], ...}
        """
        qs, pms = np.array(list(zip(*[[q, pm] for _, q, pm in self.pms])))
        params = {}
        for method in self.methods:
            if method == 'moment':
                params[method] = self.param_moment
                continue

            # qs实测流量， pms实测流量相对应的经验频率。
            avg_moment = self.param_moment[-1]
            if self.is_fit_avg:
                init_param = self.param_moment
            else:
                init_param = self.param_moment[:-1]
            # 适线寻优
            optimization_result = scipy.optimize.leastsq(
                self.__optimize_goal_fit, np.array(init_param),
                args=(qs, pms, avg_moment, method),
            )

            if optimization_result[-1] in [1, 2, 3, 4]:
                if self.is_fit_avg:
                    params[method] = [*optimization_result[0]]
                else:
                    params[method] = [*optimization_result[0], avg_moment]
            else:
                params[method] = self.param_moment
        self.param = params[self.methods[0]]
        return params

    @property
    def result(self):
        """
        设计流量结果
        :return: 每个单元为一个列表[频率p, 模比系数Kp, 设计流量Q]，注意：结果中频率p不是百分数。
        """
        result = {}
        params = self.params
        ps = self.ticks_array
        param = self.param
        for method in self.methods:
            self.param = params[method]
            qs = self.calc_q(ps)
            kps = qs / self.param[-1]
            result[method] = [[p, kps[i], qs[i]] for i, p in enumerate(ps)]
        self.param = param  # 恢复原来对象的使用参数
        return result

    def set_manual_param(self, cv, cs, avg, current_param=False):
        """
        手动设置参数（根据经验调整参数进行适线）
        :param cv: float 变差系数
        :param cs: float 偏态系数
        :param avg: float 均值
        :param current_param: boolean 是否将此组参数设置为对象的当前使用参数，默认为不设置
        """
        self.params['manual'] = [cv, cs, avg]
        if current_param:
            self.param = [cv, cs, avg]

    def _draw_scatter(self):
        # 绘制连续洪水系列散点
        pms = np.array(self.pms).T
        plt.scatter(self.norm.ppf(pms[2]) - self.U, pms[1], c='#000000', s=10, zorder=3, label="\n实测历年最大洪水\n")

    def draw_curve(self, *args, **kwargs):
        fig = self.create_figure(*args, **kwargs)
        param = self.param
        self._draw_scatter()
        for i, x in enumerate(self.params.values()):
            self.param = x
            super().draw_curve(
                color=self.colors[i], linewidth=0.5 + 1.5 / len(self.params), alpha=0.8 + 0.2 / len(self.params)
            )
        self.param = param  # 恢复原来对象的使用参数
        return fig


class PearsonThreeDiscontinuousFit(PearsonThreeContinuousFit):
    """水文频率计算(不连续系列),由于继承自P-III 曲线类，可以进行P-III 曲线相关计算"""

    def __init__(self, floods, survey_floods, N, l, methods='fit1', is_fit_avg=True):
        """
        :param floods: list n*2 array like [(年份int, 洪水流量float), ……]  实测连续系列洪水资料
        :param survey_floods: list n*2 array like [(年份int, 洪水流量float), ……]  历史调查特大洪水资料
        :param N: int 重现期
        :param l: int 连续系列中的特大洪水项数
        :param method: str or list 估计参数的方法
                            "moment"->直接使用矩法；
                            "fit1"->适线法_离差平方和准则，采用矩法初步估计，然后适线(默认)；
                            "fit2"->适线法_离差绝对值和准则，采用矩法初步估计，然后适线；
                            "fit3"->适线法_相对离差平方和准则，采用矩法初步估计，然后适线。
                            "all" -> 以上所有方法对比
        :param is_fit_avg: bool 适线时是否对均值进行寻优。True表示对均值寻优(默认)，False表示采用矩法计算的均值。
                            在 method设置为非"moment"时生效。
        """
        self.survey_floods = sorted(survey_floods, key=itemgetter(1), reverse=True)
        self.N = N
        self.l = l

        # 所有洪水资料，包含连续系列和不连续系列
        self.all_floods = sorted(floods + survey_floods, key=itemgetter(1), reverse=True)
        # 特大洪水个数(包含历史调查和连续系列中选取的)
        self.a = len(survey_floods) + l
        # 连续洪水序列个数
        self.n = len(floods)
        # 特大洪水(包含历史调查和连续系列中选取的)
        self.extra_floods = sorted(
            survey_floods + sorted(floods, key=itemgetter(1), reverse=True)[0:l], key=itemgetter(1), reverse=True
        )
        # 特大洪水的年份(包含历史调查和连续系列中选取的)
        self.extra_floods_years = [year for year, _ in self.extra_floods]

        super().__init__(floods, methods, is_fit_avg)

    def _calc_pms(self):
        # 特大洪水经验频率
        pm_d = [(year, q, (i + 1) / (self.N + 1)) for i, (year, q) in enumerate(self.all_floods) if
                year in self.extra_floods_years]

        # n-l 个连续洪水的经验频率
        pm_c = [(year, q,
                 self.a / (self.N + 1) + (1 - self.a / (self.N + 1)) * (i + 1 - self.l) / (self.n - self.l + 1))
                for i, (year, q) in enumerate(self.floods) if year not in self.extra_floods_years]

        # 整合经验频率
        pms = sorted([*pm_c, *pm_d], key=itemgetter(2))
        return pms

    def _calc_param_moment(self):
        # 实测洪水列表 l+1, ……，n
        q_cs = [q for year, q in self.floods if year not in self.extra_floods_years]

        # 特大洪水列表 1,2，……，a 个
        q_bs = [q for year, q in self.extra_floods]

        # 平均流量
        qa = 1 / self.N * (np.sum(q_bs) + (self.N - self.a) / (self.n - self.l) * np.sum(q_cs))

        # 变差系数
        cv = 1 / qa * np.sqrt(1 / (self.N - 1) * (
                np.sum([(q_b - qa) ** 2 for q_b in q_bs]) + (self.N - self.a) / (self.n - self.l) * np.sum(
            [(q_c - qa) ** 2 for q_c in q_cs])))

        # 偏态系数
        cs = self.N * (np.sum([(q_b - qa) ** 3 for q_b in q_bs]) + (self.N - self.a) / (self.n - self.l) * np.sum(
            [(q_c - qa) ** 3 for q_c in q_cs])) / ((self.N - 1) * (self.N - 2) * qa ** 3 * cv ** 3)
        return [cv, cs, qa]

    def _draw_scatter(self):
        # 绘制连续洪水系列散点
        survey_years = list(zip(*self.survey_floods))[0]
        star_pms = np.array([[year, q, pm] for year, q, pm in self.pms if year in survey_years]).T
        pms = np.array([[year, q, pm] for year, q, pm in self.pms if year not in survey_years]).T
        plt.scatter(self.norm.ppf(pms[2]) - self.U, pms[1], c='#000000', s=10, zorder=3, label="\n实测历年最大洪水\n")
        plt.scatter(self.norm.ppf(star_pms[2]) - self.U, star_pms[1], c='#808080', s=25, zorder=3, marker="*",
                    label="\n调查历史特大洪水\n")


if __name__ == '__main__':
    year1 = list(range(1985, 1952, -1))
    q1 = [
        114, 118, 116, 105, 122, 88.8, 141,
        132, 107, 94.8, 94, 113, 114, 101, 104, 92.8, 97.1,
        116, 122, 145, 119, 111, 83.1, 93.5, 104, 88.5, 95.3,
        92.5, 115, 94.5, 107, 90.9, 89.1
    ]

    data1 = {
        'methods': 'all',
        'floods': list(zip(year1, q1)),
    }

    year2 = list(range(1955, 1981))
    q2 = [
        215, 1930, 2860, 368, 193, 5670,
        1330, 338, 427, 2180, 4050, 837, 69.7, 276,
        355, 200, 561, 1260, 298, 515, 383, 79.7,
        190, 67.6, 608, 640
    ]

    data2 = {
        'floods': list(zip(year2, q2)),
        'N': 90,  # 重现期
        'survey_floods': [(1896, 4400), (1914, 4900)],
        'l': 2,
        'methods': 'all'
    }
    p = PearsonThreeContinuousFit(**data1)
    p.show()

    p2 = PearsonThreeDiscontinuousFit(**data2)
    p2.show()

