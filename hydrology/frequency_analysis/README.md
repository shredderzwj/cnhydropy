# 水文频率分析计算（使用方法） 

<center> 作者 周伟杰 </center>

## 模块 cnhydropy.hydrology.frequency_analysis API
+ 水文频率分析计算模块（P-III曲线）
+ 主要参考《水利水电工程水文计算规范》（DL T 5431-2009）、《水利水电工程设计洪水计算规范》（SL44-2006）
+ 开发环境 python3.6
+ 使用的第三方包 matplotlib,numpy,scipy
    

### 功能概述
&ensp;本程序可一次完成一个水文系列频率计算的全部工作，对连序系列和不连序系列均为适用，根据输入的数据自动判断连序系列和不连序系列。本程序完成的工作内容包括：系列排队、计算经验频率及统计参数值、通过优选P-Ⅲ型曲线的参数$C_v, C_s$值进行适线或用目估法适线、绘制频率曲线图、计算所采用的频率曲线的各设计频率下的设计值等。本程序可以计算特长系列。
    
为满足工程的实际需要，本程序除可用优选统计参数的方法适线外，还可用目估适线法进行适线。因为本程序在用优选法适线时，对各经验点据是给以等权重的处理。而当需要对各点据给以非等权重的处理时（如：设计洪水中要求多照顾首几项洪水；在年径流计算时要多照顾末端；或由于基本资料精度差等），单用优选法就不合适，此时可改用目估适线法。为了减少目估适线时的盲目性，实际使用时，一般采用优选与目估适线相结合的方法，即先用优选法选出一条通过点群中心的频率曲线。在此基础上再用目估的方法对优选出的参数$C_v, C_s$做少许调整，重新适线，以达到对各点据给以不同权重的目的，获得满意的结果。本程序在一张图上可绘多条频率曲线（用彩色加以区别），以供适线之用。

### class PearsonThree(cv, cs, avg=1)

+ base object

+ 假设已知皮尔逊三型曲线的各统计参数，进行相关计算及绘图。

#### 初始化参数：
+ :param cv: float 变差系数
+ :param cs: float 偏态系数
+ :param avg: float 均值（若单纯计算模比系数Kp，此项可不指定）

#### 属性
+ param 统计参数 list [Cv, Cs, 均值]，可设置

+ distribution 使用 param 统计参数的 scipy.stats.gamma 实例对象， 不可设置！ 

+ ticks 设置绘图频率轴的刻度（默认值是经过优化的，一般情况下不建议重新设置）, 单位为%，1表示频率为1%；格式为 ['.01', '1', ……] 或 [.1, .2, 1, ……]，最好为数字字符串，这样显示出来的与指定的完全一样，如果为数字，由于浮点数在计算机表示不是完全相等，会导致显示异常，例如 0.1 显示为 0.099999999999

    范例：['.01', '.02', '.05', '0.1', '0.2', '0.5', '1', '2', '5', '10', '20', '30', '40', '50', '60', '70', '80', '90', '95', '98', '99', '99.7', '99.9', '99.97', '99.99']

#### 方法：
+ def calc_q(p):
		
    计算指定频率的洪水流量

    :param p: float 频率（注意是小数不是百分数）

    :return: float 流量

+ def calc_kp(p):

    计算指定频率的模比系数 Kp 值。

    :param p:  float 频率（注意是小数不是百分数）

    :return: kp float 模比系数 Kp 值

+ def draw_curve(self, color=None, linewidth=2.0, alpha=1.0):
    绘制拟合的曲线

    :param color: str 曲线颜色

    :param linewidth: float 线宽

    :param alpha: float 透明度，取值范围为[0,1]，0位完全透明，1为完全不透明

    :return: matplotlib.pyplot.figure 绘图对象，可利用此接口进行自定义保存图像等操作

+ def show()
    显示绘图

+ def save(path, format='png', figsize=(15.3, 9.2), dpi=96)

    将图保存至文件

    :param path: 文件保存路径。

    :param format: str 图片文件格式（默认保存为png图片，详细支持格式见 matplotlib 文档）

    :param figsize: tuple 设置保存图片尺寸

    :param dpi: int 设置保存图片的dpi

#### 静态方法
+ def handle_floods_from_excel(data)

    处理从Excel表格中（或者其他文件）复制过来的数据，使之符合PearsonThreeContinuousFit初始化参数输入的floods值的格式。

    :param data: str 复制的数据。数据要求：第一列为年份，第二列为洪水流量值，中间以【空格、逗号、制表符、冒号、分号、星号、at符号、感叹号、竖线、斜杠线、井号】等分隔，每行一组数据。

    :return: list [(年份int, 洪水流量float), ……]

+ def get_distribution(cv, cs, avg)

    获取gamma分布对象

    :param cv: float 变差系数

    :param cs: float 偏态系数

    :param avg: float 均值（若单纯计算模比系数Kp，此项可不指定）

    参考[https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.gamma.html?highlight=gamma](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.gamma.html?highlight=gamma)

    标准 Gamma 分布 ：
$$
f(x,a) = \frac{x^{a-1}e^{-x}}{\Gamma (a)}
$$

使用$loc$和$scale=\frac{1}{\beta}$参数，对标准Gamma分布进行移动或缩放操作，则分布函数为：

$$
\begin{align}
gamma.pdf(x, a, loc, scale) &= \frac{f(\frac{x - loc}{scale}, a)}{sacle} \\\\
     &= \frac{\beta^a \cdot (x - loc)^{a-1} \cdot e^{-\beta(x-loc)}} {\Gamma(a)}
\end{align}

$$

可推出：P-III曲线三参数$[C_v, C_s, avg]$与Gamma分布三参数$[a, loc, scale]$换算关系：

$$
a = \frac{4}{C_s^2}
$$

$$
loc = avg \cdot (1- \frac{2C_v}{C_s})
$$

$$
scale = \frac{avg \cdot C_v \cdot C_s}{2}
$$

### class PearsonThreeContinuousFit(floods, methods='moment', is_fit_avg=True)

+ base PearsonThree
+ 水文频率计算(连序系列),由于继承自P-III 曲线类，可以进行P-III 曲线相关计算，计算方法来自（SL44-2006《水利水电工程设计洪水计算规范》）

#### 初始化参数
+ :param floods: list n*2 array like [(年份int, 洪水流量int), ……]  实测连序系列洪水资料
+ :param method: str or list 估计参数的方法
        "moment"->直接使用矩法(默认)；
	"fit1"->适线法_离差平方和准则，采用矩法初步估计，然后适线；
	"fit2"->适线法_离差绝对值和准则，采用矩法初步估计，然后适线；
	"fit3"->适线法_相对离差平方和准则，采用矩法初步估计，然后适线。
+ :param is_fit_avg: bool 适线时是否对均值进行寻优。True表示对均值寻优(默认)，False表示采用矩法计算的均值。
			在 method设置为非"moment"时生效。

#### 属性
+ methods 估计参数的方法， 可重新设置

+ is_fit_avg 适线时是否对均值进行寻优，可重新设置

+ param 当前对象使用的统计参数 [Cv, Cs, 均值]，当有多个估计参数的方法时，默认使用第一个方法计算的参数值。可重新设置。

    tips: calc_q和calc_kp方法，distribution和result属性，曲线绘制，均采用此参数进行后续计算

+ param_moment 矩法计算的统计参数，不可设置

+ pms 经验频率计算结果，不可设置

+ params 各种方法计算的统计参数结果，不可设置

+ result 所有估计参数的方法计算的统计参数相应的设计洪水结果，每个单元为一个列表[频率p, 模比系数Kp, 设计流量Q]

#### 方法：
+ def set_manual_param(cv, cs, avg, current_param=False)

    手动设置参数（根据经验调整参数进行适线）

    :param cv: float 变差系数

    :param cs: float 偏态系数

    :param avg: float 均值

    :param current_param: boolean 是否将此组参数设置为对象的当前使用参数（即设置对象的param属性为此参数），默认为不设置

##### 以下方法和属性继承自 PearsonThree 类 ，使用方法一致
**1. 属性**

+ distribution
+ ticks

**2. 方法**

+ def calc_q(p):		
+ def calc_kp(p):
+ def draw_curve(color=None, linewidth=2.0, alpha=1.0)
+ def show()
+ def save(path, format='png', figsize=(15.3, 9.2), dpi=96, *args, **kwargs)

### class PearsonThreeDiscontinuousFit(floods, survey_floods, N, l, methods='fit1', is_fit_avg=True)
水文频率计算(不连序系列)

#### 初始化参数
+ :param floods: list n*2 array like [(年份int, 洪水流量int), ……]  实测连序系列洪水资料
+ :param survey: survey_floods: list n*2 array like [(年份int, 洪水流量int), ……]  历史调查特大洪水资料
+ :param N: int 重现期
+ :param l: int 连序系列中的特大洪水项数
+ :param method: str or list 估计参数的方法
        "moment"->直接使用矩法(默认)；
	"fit1"->适线法_离差平方和准则，采用矩法初步估计，然后适线；
	"fit2"->适线法_离差绝对值和准则，采用矩法初步估计，然后适线；
	"fit3"->适线法_相对离差平方和准则，采用矩法初步估计，然后适线。
+ :param is_fit_avg: bool 适线时是否对均值进行寻优。True表示对均值寻优(默认)，False表示采用矩法计算的均值。
			在 method设置为非"moment"时生效。

**对外开放的使用参数和方法均继承自 PearsonThreeContinuousFit 类 ，使用方法一致**


