"""
推理公式法计算设计洪水。适用于山丘区流域面积小于200平方公里的河流
"""
from collections import defaultdict

import numpy as np

from cnhydropy.common import plt
from cnhydropy.hydrology.stream_flood_henan.relationship import Relationship


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
            q = (q + qm) / 2
            tau = 0.278 * self.L / (
                    self.m * self.J ** (1 / 3) * q ** 0.25
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
    def __init__(self, net_rain: dict, qm: float, tau: float, F: float, R: float):
        """
        :param net_rain: list 净雨过程
        :param qm: float 洪峰流量
        :param tau: float 汇流时段
        :param F: float 流域面积，km2
        :param R: float 设计净雨，mm
        """
        self.net_rain, self.qm, self.tau, self.F = net_rain, qm, tau, F
        self.R = R

    @property
    def flows(self):
        """
        洪水过程线
        :return list 数据结构为 [(t1, q1), (t2, q2), ……]
        """
        max_rain_t = sorted(self.net_rain, key=lambda x: x[1])[-1][0]
        taus = [t for t in np.arange(max_rain_t, 0, -self.tau)][1:]
        taus.reverse()
        taus += [t for t in np.arange(max_rain_t, 24 + self.tau, self.tau)]
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
        flood[min(flood.keys()) - self.tau if min(flood.keys()) - self.tau > 0 else 0] = 0
        flood[max(flood.keys()) + self.tau] = 0

        # 同倍比缩放洪量修正
        ratio = self.qm / max(flood.values())
        for t, q in flood.items():
            flood[t] = q * ratio

        # 设计洪水过程线的洪量修正
        floods = sorted(list(flood.items()), key=lambda x: x[0])
        fm = 0.278 * self.R * self.F - self.qm * self.tau
        fz = 0
        for i, f in enumerate(floods[1:]):
            fz += (f[1] + floods[i-1][1]) * self.tau / 2
        fz -= self.qm * self.tau
        ratio = fm / fz
        for t, q in flood.items():
            if not np.abs(q - self.qm) < 1e-2:
                flood[t] = q * ratio if q * ratio < self.qm else self.qm

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
        return sorted(list(hourly_r.items()), key=lambda x: x[0])

    @property
    def w(self):
        """由暴雨径流关系（设计净雨）计算的洪量"""
        return 1000 * self.R * self.F

    @property
    def w1(self):
        """由洪水过程线计算的洪量"""
        flows = self.flows
        s = 0
        for i, flow in enumerate(flows[:-1]):
            a = flow[1]
            b = flows[i + 1][1]
            h = flows[i + 1][0] - flow[0]
            s += (a + b) * h * 3600 / 2
        return s

    def create_figure(self, figsize=(12.8, 7.2), title=None):
        """创建绘制曲线的figure对象"""
        if hasattr(self, 'fig'):
            return self.fig
        if title is None:
            title = '洪水过程线'
        self.fig = plt.figure(title, figsize=figsize)
        plt.title(title, {"size": 16})
        plt.xlabel('历时$\\tau(h)$', {'size': 14})
        plt.ylabel('流量($m^3/s$)', {'size': 14})
        plt.grid(linestyle='--', linewidth=1, zorder=1)
        flood = self.flows
        x, y = zip(*flood)
        plt.plot(x, y)
        plt.xticks([i for i in range(int(flood[-1][0]) + 2)])
        return self.fig

    def show(self, *args, **kwargs):
        """显示绘图"""
        if not hasattr(self, 'fig'):
            self.create_figure(*args, **kwargs)
        plt.show()
        plt.cla()
        plt.close()
        delattr(self, 'fig')

    def save(self, path, format='png', dpi=96, figsize=(12.8, 7.2), title=None, **kwargs):
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


if __name__ == '__main__':
    # 导包
    from cnhydropy.hydrology.stream_flood_henan.stream import Stream, DesignStream
    from cnhydropy.hydrology.stream_flood_henan.relationship import RelationshipPRHills
    from cnhydropy.hydrology.stream_flood_henan.relationship import RelationshipThetaM

    """输入流域特征属性，计算暴雨参数"""
    F = 72              # 流域面积
    L = 18              # 河道长度
    J = 0.003          # 河道平均比降
    coord = (113, 34)   # 流域重心坐标
    stream = Stream(*coord)     # 暴雨参数对象（只与流域特征相关，也就是查图集得到的参数）

    """指定设计频率，计算设计暴雨参数"""
    p = 1 / 100  # 设计频率
    design_stream = DesignStream(stream, F, p, project_type=1)  # 设计暴雨参数对象
    design_hf_1h = design_stream.design_hf_1h  # 设计1小时雨量
    hourly_net_rain = design_stream.hourly_net_rain()  # 逐时净雨
    pa = RelationshipPRHills().pa(design_stream.area, p)  # 前期影响雨量
    R = RelationshipPRHills().R(design_stream.area,
                                pa + design_stream.design_hf_24h)  # 设计净雨
    n1 = design_stream.n1
    n2 = design_stream.n2
    n3 = design_stream.n3

    """计算设计流量及汇流时间"""
    mu = design_stream.mu  # 平均入渗强度
    theta = RelationshipThetaM().theta(F, L, J)  # θ流域特征系数
    m = RelationshipThetaM().m(stream.area, theta)  # 汇流参数
    peak_flow = ReasoningPeakFlow(F, L, J, design_hf_1h, n1, n2, n3, mu, m)
    qm = peak_flow.qm       # 洪峰流量
    tau = peak_flow.tau     # 洪峰汇流时间

    """计算洪水过程线"""
    flood_process = FloodProcess(hourly_net_rain, qm, tau, F, R)

    """展示结果"""
    print('-'*20, '暴雨参数(查图结果)', '-'*20)
    stream.show_param()
    print('\n')

    print('-'*20, '设计暴雨', '-'*20)
    design_stream.show_param()
    print('\n')

    print('-' * 20, '洪水过程线', '-' * 20)
    print('\t时间\t流量m3/s')
    for (t, q) in flood_process.flood():
        print('\t%d\t%.2f' % (int(t), float(q)))
    print('\n')
    print('流域特征系数θ：%.2f' % theta)
    print('汇流参数m：%.2f' % m)
    print('洪峰径流系数Ψ：%.2f' % peak_flow.psi)
    print('洪峰汇流时间τ：%.2f h' % tau)
    print('洪峰流量Qm：%.2f m3/s' % qm)
    print('设计净雨计算洪量W：%.2f 万m3' % (flood_process.w / 10000))
    print('洪水过程计算洪量W：%.2f 万m3' % (flood_process.w1 / 10000))

    flood_process.show()



