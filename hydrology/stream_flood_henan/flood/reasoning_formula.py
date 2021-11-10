"""
推理公式法计算设计洪水。适用于山丘区流域面积小于200平方公里的河流
"""
from collections import defaultdict

import numpy as np
import matplotlib.pyplot as plt
# plt.switch_backend('qt5agg')  # 切换 matplotlib 绘图后端为agg。
# 设置 matplotlib 字体，解决中文乱码的问题（linux平台需要安装 SimHei 字体，macOS没用过）
plt.rcParams['font.family'] = ['sans-serif']
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

from ..relationship import Relationship


class ReasoningPeakFlow(object):
    _Qm = None
    _tau = None
    _psi = None

    def __init__(self,
        F: float, L: float, J: float, S: float,
        n1: float, n2: float, n3: float, mu: float, m: float
    ):
        """
        :param F: float 流域面积（km2）
        :param L: float 干流长度，设计断面至干流分水岭（km）
        :param J: float L的平均坡度（以小数计）
        :param S: float 设计最大1小时雨量平均值，即设计频率1小时雨量（mm/h）
        :param n1: float 暴雨递减指数（小于1小时）
        :param n2: float 暴雨递减指数（1~6小时）
        :param n3: float 暴雨递减指数（6~24小时）
        :param mu: float 平均入渗率，以mm/h计
        :param m: float 汇流参数
        """
        self.F, self.L, self.J, self.S = F, L, J, S
        self.n1, self.n2, self.n3 = n1, n2, n3
        self.mu, self.m = mu, m

    def n(self, tau):
        if tau < 1:
            return self.n1
        elif 1 <= tau < 6:
            return self.n2
        else:
            return self.n3

    def peak_flow(self):
        """设计洪峰流量"""
        q = 1
        qm = 1e20
        tau = 1
        psi = 1
        while np.abs(q - qm) > 1e-3:
            q = (q + qm) / 2.0
            tau = 0.278 * self.L / (
                    self.m * self.J**(1.0 / 3.0) * q**0.25
            )
            psi = 1 - self.mu * tau**self.n(tau) / self.S
            qm = 0.278 * psi * self.S * self.F / tau**self.n(tau)
        if qm < 0:
            raise ValueError('可能参数有误，最终计算的流量竟然为负值！！！')
        self._Qm = qm
        self._tau = tau
        self._psi = psi

    @property
    def qm(self):
        """洪峰流量"""
        if self._Qm is None:
            self.peak_flow()
        return self._Qm

    @property
    def tau(self):
        """洪峰汇流时间"""
        if self._tau is None:
            self.peak_flow()
        return self._tau

    @property
    def psi(self):
        """径流系数"""
        if self._psi is None:
            self.peak_flow()
        return self._psi


class FloodProcess(object):
    """洪水过程"""
    def __init__(self, p: float, net_rain: list, qm: float, tau: float, F: float, R: float):
        """
        :param p: float 频率
        :param net_rain: list 净雨过程
        :param qm: float 洪峰流量
        :param tau: float 汇流时段
        :param F: float 流域面积，km2
        :param R: float 设计净雨，mm
        """
        self.p, self.net_rain, self.qm, self.tau, self.F = p, net_rain, qm, tau, F
        self.R = R

    @property
    def flows(self):
        """
        洪水过程线
        :return list 数据结构为 [(t1, q1), (t2, q2), ……]
        """
        import pprint
        max_rain_t = sorted(self.net_rain, key=lambda x: x[1])[-1][0]
        taus = [t for t in np.arange(max_rain_t, 0, -self.tau)][1:]
        taus.reverse()
        taus += [t for t in np.arange(max_rain_t, 24 + self.tau, self.tau)]
        net_rain = {int(rain[0]): rain[1] for rain in self.net_rain}
        net_rain[0] = 0
        net_rains = [rain[1] for rain in self.net_rain]
        R = defaultdict(float)
        for i, t in enumerate(taus):
            if i == 0:
                R[t] = sum(net_rains[:int(t)]) + net_rains[int(t)] * (t - int(t))
            else:
                if t < 24:
                    R[t] = net_rains[int(taus[i - 1])] * (1+int(taus[i - 1])-taus[i - 1]) + \
                           sum(net_rains[int(taus[i - 1]) + 1:int(t)]) + \
                           net_rains[int(t)] * (t - int(t))
                else:
                    R[t] = net_rains[int(taus[i - 1])] * (1+int(taus[i - 1])-taus[i - 1]) + \
                           sum(net_rains[int(taus[i - 1]) + 1:])

        flood = {t: 0.278*r*self.F / self.tau for t, r in R.items() if r > 0}
        # flood[0] = 0
        flood[min(flood.keys()) - self.tau if min(flood.keys()) - self.tau > 0 else 0] = 0
        flood[max(flood.keys()) + self.tau] = 0

        # 同倍比缩放修正洪峰
        # ratio = self.qm / max(flood.values())
        # for t, q in flood.items():
        #     flood[t] = q * ratio

        # 修正洪峰
        ts, qs = zip(*flood.items())
        qm_t = ts[qs.index(max(qs))]  # 洪峰出现的时段
        flood[qm_t] = self.qm
        return sorted(list(flood.items()), key=lambda x: x[0])

    def flood(self, t: float = None):
        """
        逐时洪水过程线
        :param t: float 过程线时间间隔
        :return: list 数据结构为 [(t1, q1), (t2, q2), ……]
        """
        if t is None:
            t = 1

        r = Relationship(self.flows)
        hourly_r = {}
        for i in np.arange(0, int(r.points[-1][0]) + 2, t):
            hourly_r[i] = r(i)
        qm_t, qm = sorted(r.points, key=lambda x: x[1])[-1]
        hourly_r[qm_t] = qm

        # 设计洪水过程线的洪量修正
        flows = sorted(list(hourly_r.items()), key=lambda x: x[0])
        w1 = self.calc_process_w(flows)
        ratio = (self.wRF - t * 3600.0 * self.qm) / (w1 - t * 3600.0 * self.qm)

        flows_result = []
        for t, q in flows:
            if abs(qm_t - t) < 1e-8:
                flows_result.append((qm_t, self.qm))
                continue
            flows_result.append((t, q*ratio))
        return flows_result

    @property
    def wRF(self):
        """由暴雨径流关系（设计净雨）计算的洪量"""
        return 1000.0 * self.R * self.F

    @staticmethod
    def calc_process_w(flows):
        s = 0
        for i, flow in enumerate(flows[:-1]):
            a = flow[1]
            b = flows[i + 1][1]
            h = flows[i + 1][0] - flow[0]
            s += (a + b) * h * 3600.0 / 2.0
        return s

    @property
    def w(self):
        """由洪水过程线计算的洪量"""
        flows = self.flood()
        return self.calc_process_w(flows)

    def create_figure(self, figsize=(9.6, 5.4), title=None, xlabel=None, ylabel=None):
        """创建绘制曲线的figure对象"""
        if hasattr(self, 'fig'):
            return self.fig
        if title is None:
            title = '设计洪水过程线(设计频率：%.2f%%)' % (self.p*100)
        self.fig = plt.figure(title, figsize=figsize)
        plt.title(title, {"size": 15})
        plt.xlabel(xlabel if xlabel else '历时$\\tau(h)$', {'size': 13})
        plt.ylabel(ylabel if ylabel else '流量($m^3/s$)', {'size': 13})
        plt.grid(linestyle='--', linewidth=1, zorder=1)
        flood = self.flows
        x, y = zip(*flood)
        max_q = max(y)
        max_q_x = x[y.index(max_q)]
        plt.text(max_q_x, max_q, '$Q_m=%.2fm^3/s$  $W=%.2f$万$m^3$' % (max_q, self.w*1e-4), {'size': 11})
        plt.plot(x, y)
        plt.xticks([i for i in range(int(flood[-1][0]) + 2)])
        # plt.legend('设计频率：%.2f%%' % (self.p*100))
        return self.fig

    def show(self, *args, **kwargs):
        """显示绘图"""
        plt.cla()
        plt.close()
        if not hasattr(self, 'fig'):
            self.create_figure(*args, **kwargs)
        self.fig.show()
        delattr(self, 'fig')

    def save(self, path, format='png', dpi=96, figsize=(9.6, 5.4), title=None, **kwargs):
        """
        将图保存至文件
        :param path: 文件保存路径。
        :param format: str 图片文件格式， 详细支持格式见 matplotlib 文档
        :param dpi: int 设置保存图片的dpi
        :param figsize: tuple 设置保存图片尺寸
        :param title: str 图标题
        """
        if hasattr(self, 'fig'):
            plt.cla()
            plt.close()
            delattr(self, 'fig')
        self.create_figure(figsize=figsize, title=title)
        self.fig.set_size_inches(*figsize)
        self.fig.savefig(path, format=format, dpi=dpi, bbox_inches='tight', **kwargs)  # transparent=True)
        plt.cla()
        plt.close()
        delattr(self, 'fig')



