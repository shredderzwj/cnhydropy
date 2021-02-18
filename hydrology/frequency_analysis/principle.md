# 水文频率分析计算（原理）

<div style="text-align: center;"> 作者 周伟杰 </div>

[TOC]

## 计算依据
《水利水电工程水文计算规范》（DL T 5431-2009）、《水利水电工程设计洪水计算规范》（SL44-2006）

## 计算方法
* 采用矩法初步估算统计参数;
* 采用适线法调整初步估算的统计参数。调整时，采用选定目标函数求解统计参数。
* 也可采用经验适线法，调整参数，尽可能拟合全部点据，拟合不好时，可侧重考虑较可靠的大洪水点据。

## 一、矩法

### 1. n年连序系列
#### ① 经验频率计算

$$p_m = \frac{m}{n+1}$$

式中：

&ensp;&ensp;&ensp;&ensp;
$n$——洪水系列项数；

&ensp;&ensp;&ensp;&ensp;
$m$——洪水连序系列中的序位（$m=1,2,…,n$）；

&ensp;&ensp;&ensp;&ensp;
$P_m$——第$m$项洪水的经验频率。

#### ② 洪水频率曲线统计参数计算

可采用下列公式计算各统计参数：

$$ \overline{X} = \frac1n \sum_{i=1}^{n}{X_i}$$

$$S = \sqrt{\frac1{n-1} \sum_{i=1}^n{(X_i - \overline{X}})^2}$$

$$C_v = \frac{S}{\overline{X}}$$

$$C_s = \frac{n \sum_{i=1}^n {(X_i-\overline{X})^3}} {(n-1)(n-2) \overline{X}^3 C_v^3}$$


式中：

&ensp;&ensp;&ensp;&ensp;
$\overline{X}$——系列均值；

&ensp;&ensp;&ensp;&ensp;
$S$——系列均值；

&ensp;&ensp;&ensp;&ensp;
$C_v$——变差系数；

&ensp;&ensp;&ensp;&ensp;
$C_s$——偏态系数；

&ensp;&ensp;&ensp;&ensp;
$X_i$——系列变量（$i=1, 2, …,n$）；

&ensp;&ensp;&ensp;&ensp;
$n$——系列项数。

### 2. 不连序系列
#### ① 经验频率计算

在调查考证期$N$年中有特大洪水$a$个，其中$l$个发生在$n$项连序系列内，这类不连序洪水系列中各项洪水的经验频率可采用下列数学期望公式计算：

$$P_M = \frac{M}{N+1}$$

$$P_m = \frac{a}{N+1}+\left(1-\frac{a}{N+1}\right)\frac{m-l}{n-l+1}$$

式中：

&ensp;&ensp;&ensp;&ensp;
$M$——特大洪水序位（$M=1,2,…,a$）；

&ensp;&ensp;&ensp;&ensp;
$P_M$——第$M$项特大洪水经验频率；

&ensp;&ensp;&ensp;&ensp;
$N$——历史洪水调查考证期；

&ensp;&ensp;&ensp;&ensp;
$a$——特大洪水个数；

&ensp;&ensp;&ensp;&ensp;
$l$——从$n$项连序系列中抽出的特大洪水个数。

&ensp;&ensp;&ensp;&ensp;
$m$——洪水连序系列中的序位（$m=l+1,…,n$）；

&ensp;&ensp;&ensp;&ensp;
$P_m$——第$m$项洪水的经验频率。

#### ② 洪水频率曲线统计参数计算

如果在迄今的N年中已查明有$a$个特大洪水（其中有$l$个发生在$n$年实测或插补系列中），假定（$n-l$）年系列的均值和均方差与除去特大洪水后的（$N-a$）年系列的均值和均方差分别相等，即$\overline X_{N-a} = \overline X_{n-l}$, $S_{n-a} = S_{n-l}$，可推导出统计参数的计算公式如下：

$$\overline{X} = \frac1n\left(\sum_{j=1}^aX_j+\frac{N-a}{n-l}\sum_{i=l+1}^nX_i\right)$$

$$C_v = \frac1X\sqrt{\frac1{N-1}\left[\sum_{j=1}^a(X_j-\overline{X})^2 + \frac{N-a}{n-l}\sum_{i=l+1}^n(X_i-\overline{X})^2\right]}$$

$$C_s=\frac{N\left[\sum_{j=1}^a(X_j-\overline{X})^3 + \frac{N-a}{n-l}\sum_{i=l+1}^n(X_i-\overline{X})^3\right]} {(N-1)(N-2)\overline{X}^3C_v^3}$$

式中：

&ensp;&ensp;&ensp;&ensp;
$X_j$——特大洪水变量（$j=1,2,…,a$）；

&ensp;&ensp;&ensp;&ensp;
$X_i$——实测洪水变量（$j=1,2,…,a$）；

&ensp;&ensp;&ensp;&ensp;
$N$——历史洪水调查考证期；

&ensp;&ensp;&ensp;&ensp;
$a$——特大洪水个数；

&ensp;&ensp;&ensp;&ensp;
$l$——从$n$项连序系列中抽出的特大洪水个数。

## 二、适线法
适线法的特点是在一定的适线准则下，求解与经验点据拟合最优的频率曲线的统计参数。一般可根据洪水系列的误差规律，选定适线准则。

* 当系列中各项洪水的误差方差比较均匀时， 可考虑采用离（残）差平方和准则

* 当绝对值误差比较均匀时，可考虑采用离（残）绝对值和准则

* 当各项洪水（尤其是历史洪水）误差差别比较大时，宜采用相对离差平方和准则

### 1.离差平方和准则
也称最小二乘估计。频率曲线统计参数的最小二乘估计使经验点据和同频率的频率曲线纵坐标之差（即离差或残差）平方和达到极小。
$$S_1(\overline{X}, C_v, C_s) = \sum_{i=1}^n\left[X_i - f(P_i;\overline{X}, C_v, C_s)\right]^2$$
求得使$S_1(\overline{X}, C_v, C_s)$达到极小值的参数$\overline{X}, C_v, C_s$

### 2.离差绝对值和准则
$$S_2(\overline{X}, C_v, C_s) = \sum_{i=1}^n\left\vert X_i - f(P_i;\overline{X}, C_v, C_s)\right \vert$$
求得使$S_2(\overline{X}, C_v, C_s)$达到极小值的参数$\overline{X}, C_v, C_s$

### 3.相对离差平方和准则
考虑洪水误差和它的大小有关，而它们的相对误差却比较稳定，因此以相对离差平方和最小更符合最小二乘估计的假定。
$$S_3(\overline{X}, C_v, C_s) =\sum_{i=1}^n\left[ \frac{X_i - f(P_i;\overline{X}, C_v, C_s)} {f_i(\theta)}\right]^2 \approx \sum_{i=1}^n\left[ \frac{X_i - f_i(\theta)} {X_i}\right]^2$$
求得使$S_3(\overline{X}, C_v, C_s)$达到极小值的参数$\overline{X}, C_v, C_s$

式中：$\theta$ 为参数向量，即$\theta = (\overline{X}, C_v, C_s)^T$
 
## 三、经验适线法 
采用矩法或者其他方法估计一组参数作为初值，通过经验判断调整参数，选定一条与经验点据拟合良好的频率曲线。适线时应注意：

1. 尽可能照顾点群趋势，使频率曲线通过点群的中心，但可适当多考虑上部和中部点据。
2. 应分析经验点据的精度（包括他们的横、纵坐标），使曲线尽量地接近或通过比较可靠的点据。
3. 历史洪水，特别是为首的几个历史特大洪水，一般精度较差，适线时，不宜机械地通过这些点据，而使频率曲线脱离点群；但也不能为了照顾点群趋势使曲线离开特大值太远，应考虑特大历史洪水的可能误差范围，以便调整频率曲线。