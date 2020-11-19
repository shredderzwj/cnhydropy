# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt

# plt.switch_backend('agg')  # 切换 matplotlib 绘图后端为agg。
# 设置 matplotlib 字体，解决中文乱码的问题（linux平台需要安装 SimHei 字体，macOS没用过）
plt.rcParams['font.family'] = ['sans-serif']
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
