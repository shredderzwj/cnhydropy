# 各种形式的过水断面水力要素计算

<center class="author"> 作者 周伟杰 </center>
## 计算依据：
《水力计算手册（第二版）》 （李炜 2006 中国水利水电出版社）、《渠道防渗工程技术规范》（GB T 50600-2010）

## 符号含义
* $B$ —— 水面宽
  
* $b$ —— 底宽

* $m$ —— 坡度系数

* $r$ —— 圆弧半径

* $\theta$ —— 圆弧角度

* $H$ —— 水深

* $\chi$ —— 湿周

* $\omega$ —— 过水断面面积

* $R$ —— 水力半径

## 一、梯形断面

<center><svg xmlns="http://www.w3.org/2000/svg" width="389.899" height="200" viewBox="0 0 292.424 150"><g clip-path="url(#cp0)"><path stroke-width="1.090908" stroke-linecap="round" stroke-linejoin="round" fill="none" stroke="#000" d="M14.455 33.545h39.818l48 69.273H179.455l48-69.273h39.818M66.818 51.545H214.91M130.09 51.545h19.637M132.545 54h14.728M135 56.455h9.818M137.455 58.91h4.909M66.818 45.818V11.182M214.91 45.818V11.182M74.727 19.09h132.546"/><path d="M74.727 17.727v2.728l-7.909-1.364z"/><path stroke-width="1.090908" stroke-linecap="round" stroke-linejoin="round" fill="none" stroke="#000" d="M74.727 17.727v2.728l-7.909-1.364z"/><path d="M207.273 17.727v2.728l7.636-1.364z"/><path stroke-width="1.090908" stroke-linecap="round" stroke-linejoin="round" fill="none" stroke="#000" d="M207.273 17.727v2.728l7.636-1.364zM141.545 10.636l1.091.546.273.273.273.818v1.363l-.273.819-.273.272-1.09.546h-3V6.545h3l1.09.546.273.273.273.818V9l-.273.818-.273.546-1.09.272h-3M130.09 51.545h21.546M148.09 43.636h-15.817l7.909 7.91 7.909-7.91M218.727 102.818h27.818M218.727 51.545h27.818M238.91 94.91V59.454"/><path d="M237.545 94.91h2.728l-1.364 7.908z"/><path stroke-width="1.090908" stroke-linecap="round" stroke-linejoin="round" fill="none" stroke="#000" d="M237.545 94.91h2.728l-1.364 7.908z"/><path d="M237.545 59.455h2.728l-1.364-7.91z"/><path stroke-width="1.090908" stroke-linecap="round" stroke-linejoin="round" fill="none" stroke="#000" d="M237.545 59.455h2.728l-1.364-7.91zM235.09 79.364h-8.454M226.636 74.727h8.455M230.455 79.364v-4.637M102.273 109.364v25.09M179.455 109.364v25.09M110.182 126.818h61.636"/><path d="M110.182 125.455v2.454l-7.91-1.09z"/><path stroke-width="1.090908" stroke-linecap="round" stroke-linejoin="round" fill="none" stroke="#000" d="M110.182 125.455v2.454l-7.91-1.09z"/><path d="M171.818 125.455v2.454l7.637-1.09z"/><path stroke-width="1.090908" stroke-linecap="round" stroke-linejoin="round" fill="none" stroke="#000" d="M171.818 125.455v2.454l7.637-1.09zM139.09 122.727v-8.454M139.09 118.364l.546-.819.546-.272h1.09l.546.272.818.819.273 1.363v.818l-.273 1.091-.818.819-.545.272h-1.091l-.546-.272-.545-.819M88.636 67.09l.546.274h1.636l-7.09 4.909M90.818 72.273h-.545l-.273.545h.545l.273-.545M86.727 75h-.545v.545h.273l.272-.545M88.636 79.09l4.637-3M91.91 76.91h1.635l.546.272.545.818.273.818-.818 1.091-3.546 2.182M94.09 79.91h1.365l.818.272.545.818v.818l-.818.818-3.273 2.455"/></g></svg></center>

$$
B = b + 2Hm
$$

$$
\omega = (b + mH)H
$$


$$
\chi = b + 2H\sqrt{1+m^2}
$$

$$
R = \frac{\omega}{\chi} = \frac{(b + mH)H}{b + 2H\sqrt{1+m^2}}
$$

## 二、U形断面

<center><svg xmlns="http://www.w3.org/2000/svg" width="225" height="200" viewBox="0 0 168.75 150"><g clip-path="url(#cp0)"><path stroke-width="1.125" stroke-linecap="round" stroke-linejoin="bevel" fill="none" stroke="#000" d="M39.094 80.531l1.406 4.781 2.25 4.5 2.813 4.22 3.093 3.656 3.938 3.374 4.218 2.532 4.5 1.969 4.782 1.406 5.062.844h5.063l5.062-.844 4.781-1.406 4.5-1.97 4.22-2.53 3.937-3.375 3.094-3.657 2.812-4.219 2.25-4.5 1.406-4.78"/><path stroke-width="1.125" stroke-linecap="round" stroke-linejoin="round" fill="none" stroke="#000" d="M11.25 34.125h16.313l11.25 46.406M135.844 34.125H119.53l-11.25 46.406M117 45.375H30.375M63.563 45.375H83.25M66.094 47.906H81M68.625 50.438h9.844M70.875 52.688h5.063M63.563 45.375H85.5M81.844 37.219H65.53l8.156 8.156 8.157-8.156M58.219 75.75l-7.594 1.969M88.875 75.75l-7.594-1.687"/><path stroke-width="1.125" stroke-linecap="round" stroke-linejoin="bevel" fill="none" stroke="#000" d="M62.156 82.781l2.813 2.532L68.344 87l3.375.844h3.937L79.031 87l3.375-1.687 2.813-2.532"/><path d="M61.031 83.625l2.25-1.406-5.062-6.469z"/><path stroke-width="1.125" stroke-linecap="round" stroke-linejoin="bevel" fill="none" stroke="#000" d="M61.031 83.625l2.25-1.406-5.062-6.469z"/><path d="M84.094 82.219l2.25 1.406 2.531-7.875z"/><path stroke-width="1.125" stroke-linecap="round" stroke-linejoin="bevel" fill="none" stroke="#000" d="M84.094 82.219l2.25 1.406 2.531-7.875z"/><path stroke-width="1.125" stroke-linecap="round" stroke-linejoin="round" fill="none" stroke="#000" d="M73.688 83.906h-.563l-.281-.281-.563-.281L72 82.78l-.281-.281v-.563l-.281-.562-.282-.844v-3.094l.281-.843.282-.282v-.562l.562-.563.563-.843h.281l.562-.282.563.282.563.281.28.562.563.563v.562l.282.563.28.844V79.687l-.28.844v.844l-.282.562-.281.844-.562.563-.282.281-.281.281h-.562l-.844-.281-.563-.563L72 82.5l-.281-.844v-.562l-.281-.844v-1.688l.28-1.125v-1.125L72 75.75l.562-.844.563-.562.281-.282h.281l.563.282.563.281.28.562.282.563.281.562v1.407l.282.843v.563l-.282 1.125v.844l-.281.562-.281 1.125-.563.563-.281.562h-.562"/><path stroke-width="1.125" stroke-linecap="round" stroke-linejoin="round" fill="none" stroke="#000" d="M71.438 79.125l4.5-.562-4.5.843M30.375 34.406V11.063M117 34.406V11.063M38.25 18.938h70.875"/><path d="M38.25 17.531v2.532l-7.875-1.125z"/><path stroke-width="1.125" stroke-linecap="round" stroke-linejoin="round" fill="none" stroke="#000" d="M38.25 17.531v2.532l-7.875-1.125z"/><path d="M109.125 17.531v2.532L117 18.938z"/><path stroke-width="1.125" stroke-linecap="round" stroke-linejoin="round" fill="none" stroke="#000" d="M109.125 17.531v2.532L117 18.938zM74.25 10.5l1.125.281.281.281.281.844v1.406l-.28.844-.282.281L74.25 15h-2.813V6.281h2.813l1.125.282.281.562.281.844v.844l-.28.843-.282.282-1.125.562h-2.813M123.469 107.813h26.156M123.469 45.375h26.156M141.75 99.938V53.25"/><path d="M140.625 99.938h2.531l-1.406 7.874z"/><path stroke-width="1.125" stroke-linecap="round" stroke-linejoin="round" fill="none" stroke="#000" d="M140.625 99.938h2.531l-1.406 7.874z"/><path d="M140.625 53.25h2.531l-1.406-7.875z"/><path stroke-width="1.125" stroke-linecap="round" stroke-linejoin="round" fill="none" stroke="#000" d="M140.625 53.25h2.531l-1.406-7.875zM137.813 78.844h-8.72M129.094 74.344h8.719M133.313 78.844v-4.5M38.813 87.844v43.875M108.281 87.844v43.875M46.969 123.844h53.437"/><path d="M46.969 122.438v2.812l-8.156-1.406z"/><path stroke-width="1.125" stroke-linecap="round" stroke-linejoin="round" fill="none" stroke="#000" d="M46.969 122.438v2.812l-8.156-1.406z"/><path d="M100.406 122.438v2.812l7.875-1.406z"/><path stroke-width="1.125" stroke-linecap="round" stroke-linejoin="round" fill="none" stroke="#000" d="M100.406 122.438v2.812l7.875-1.406zM71.719 119.906v-8.719M71.719 115.406l.562-.844.844-.562h.844l.562.562.844.844.281 1.125v.844l-.281 1.125-.844.844-.562.562h-.844l-.844-.562-.562-.844"/><path d="M38.813 80.531l5.624-2.25L45 79.97z"/><path stroke-width="1.125" stroke-linecap="round" stroke-linejoin="round" fill="none" stroke="#000" d="M38.813 80.531l5.624-2.25L45 79.97zM44.719 79.125l28.968-7.031"/><path d="M108.281 80.531l-5.906-.562.281-1.688z"/><path stroke-width="1.125" stroke-linecap="round" stroke-linejoin="round" fill="none" stroke="#000" d="M108.281 80.531l-5.906-.562.281-1.688zM102.656 79.125l-28.969-7.031M53.719 75.188V69.28M53.719 71.813L54 70.686l.844-.843.562-.563h.844M41.063 50.438l.562.562 1.406.562-8.437 1.97M41.344 56.063l-.563-.282-.281.563.562.281.282-.562M36.563 57.188H36l-.281.28.281.282.562-.562M36.844 61.969l5.625-1.406M40.781 61.125l1.406.562.563.563.281.844-.281.844-1.125.562-3.937 1.125M41.625 64.5l1.406.844.563.281.281 1.125-.281.844-1.125.562L38.53 69M36 107.813H14.625M36 80.531H14.625M22.5 99.938V88.406"/><path d="M21.094 99.938h2.531l-1.125 7.874z"/><path stroke-width="1.125" stroke-linecap="round" stroke-linejoin="round" fill="none" stroke="#000" d="M21.094 99.938h2.531l-1.125 7.874z"/><path d="M21.094 88.406h2.531L22.5 80.531z"/><path stroke-width="1.125" stroke-linecap="round" stroke-linejoin="round" fill="none" stroke="#000" d="M21.094 88.406h2.531L22.5 80.531zM18.563 96h-8.72M14.344 96l-1.125-.844-.563-.844v-.843l.563-.844 1.125-.281h4.219"/></g></svg></center>

U形断面上部直线段与底部圆弧段应相切，则有关系：
$\theta = 2\cdot arccot(m)$，
$b = \frac{2r}{\sqrt{1+m^2}}$

弧形段高度 $h = r(1-\frac{m}{\sqrt{1+m^2}})$

当水深未超过下部弧形段时，即：$H \le h$，湿周所占弧形角度为：$\alpha = 2arccos \frac{r-H}{r}$

$$
B = \begin{cases} 
    2\sqrt{2Hr-H^2} & 
        \ H \le h\\
    b + 2m(H-h)& 
        \ H \gt h
\end{cases}
$$

$$
\omega=\begin{cases} 
    \frac{r^2}{2} \left(\alpha - sin\alpha \right) & 
        \ H \le h\\
    \frac{r^2}{2}\left(\theta-\frac{m}{1+m^2}\right) + \left[b + m\left(H-h\right) \right]\left(H-h\right)& 
        \ H \gt h
\end{cases}
$$

$$
\chi = \begin{cases} 
    r \cdot \alpha &
        \ H \le h\\
    r \cdot \theta + 2(H-h)\sqrt{1+m^2} & 
        \ H \gt h
\end{cases}
$$

$$
R=\frac{\omega}{\chi}
$$

## 三、圆形断面

<center><svg xmlns="http://www.w3.org/2000/svg" width="221.569" height="200" viewBox="0 0 166.176 150"><g clip-path="url(#cp0)"><path stroke-width="1.0588248" stroke-linecap="round" stroke-linejoin="bevel" fill="none" stroke="#000" d="M64.059 32.735L58.235 33l-5.559 1.059-5.558 1.588-5.294 2.382-5.03 2.912-4.765 3.441-4.235 3.97-3.706 4.5-3.176 4.766-2.647 5.294-1.853 5.294-1.324 5.559-.794 5.823v5.824l.794 5.823 1.324 5.56 1.853 5.293 2.647 5.294 3.176 4.765 3.706 4.5 4.235 3.97 4.765 3.442 5.03 2.912 5.294 2.382 5.558 1.588 5.56 1.059 5.823.265 5.823-.265 5.56-1.059L81 129.353l5.294-2.382 5.03-2.912 4.764-3.441 4.236-3.97 3.705-4.5 3.177-4.766 2.647-5.294 1.853-5.294 1.323-5.559.795-5.823v-5.824l-.795-5.823-1.323-5.56-1.853-5.293-2.647-5.294-3.177-4.765-3.705-4.5-4.236-3.97-4.764-3.442-5.03-2.912L81 35.647l-5.559-1.588L69.882 33l-5.823-.265"/><path stroke-width="1.0588248" stroke-linecap="round" stroke-linejoin="round" fill="none" stroke="#000" d="M111.97 69.265H16.148M54.53 69.265h18.794M56.912 71.647h14.03M59.294 74.03h9.265M61.676 76.147h4.5M54.794 69.265h20.647M71.735 61.588H56.647l7.412 7.677 7.676-7.677M16.147 69.265l38.647 10.588M111.97 69.265L73.325 79.853"/><path stroke-width="1.0588248" stroke-linecap="round" stroke-linejoin="bevel" fill="none" stroke="#000" d="M47.382 85.412l.794 3.176 1.589 3.177 2.117 2.647 2.647 2.117 2.912 1.589 3.177 1.058 3.44.265 3.442-.265 3.176-1.058 2.912-1.589 2.647-2.117 2.118-2.647 1.588-3.177.794-3.176"/><path d="M46.059 85.412h2.647L47.647 78z"/><path stroke-width="1.0588248" stroke-linecap="round" stroke-linejoin="bevel" fill="none" stroke="#000" d="M46.059 85.412h2.647L47.647 78z"/><path d="M79.676 85.412h2.383L80.47 78z"/><path stroke-width="1.0588248" stroke-linecap="round" stroke-linejoin="bevel" fill="none" stroke="#000" d="M79.676 85.412h2.383L80.47 78z"/><path stroke-width="1.0588248" stroke-linecap="round" stroke-linejoin="round" fill="none" stroke="#000" d="M55.324 92.559l-.265-.265v-.53l-.265-.529.265-.53v-.529l.265-.529v-.53l.529-.529.265-.53.264-.264.265-.53.53-.529.529-.53.53-.264.529-.265.53-.264h.529l.794-.265.53.265.264.264.264.265.265.794v1.06l-.265.529-.264.529-.265.794-.53.265-.529.794-.264.53-.53.264-.53.53-.793.264-.53.265-.794.265h-.794l-.53-.265-.264-.794v-.794l.265-.53v-.53l.529-.793.265-.53.53-.53.528-.793.795-.794.794-.53.53-.265.793-.264h1.588l.265.53v.793l-.265.53v.53l-.264.529-.265.529-.265.53-.53.529-.528.53-.53.793-.53.265-.793.53-.795.529-.794.265h-.53l-.528-.265"/><path stroke-width="1.0588248" stroke-linecap="round" stroke-linejoin="round" fill="none" stroke="#000" d="M60.353 89.912l-3.706-2.118 3.706 2.382M16.147 52.324v-32.03M111.97 52.324v-32.03M23.559 27.706h81"/><path d="M23.559 26.647v2.382l-7.412-1.323z"/><path stroke-width="1.0588248" stroke-linecap="round" stroke-linejoin="round" fill="none" stroke="#000" d="M23.559 26.647v2.382l-7.412-1.323z"/><path d="M104.559 26.647v2.382l7.412-1.323z"/><path stroke-width="1.0588248" stroke-linecap="round" stroke-linejoin="round" fill="none" stroke="#000" d="M104.559 26.647v2.382l7.412-1.323zM64.853 19.765l.794.53.265.264.264.794v1.059l-.264.794-.265.53-.794.264H61.94v-7.941h2.912l.794.265.265.264.264.794v.794l-.264.795-.265.529-.794.265H61.94M87.088 132.265h49.765M64.059 69.265h72.794M129.441 124.853V76.676"/><path d="M128.382 124.853h2.383l-1.324 7.412z"/><path stroke-width="1.0588248" stroke-linecap="round" stroke-linejoin="round" fill="none" stroke="#000" d="M128.382 124.853h2.383l-1.324 7.412z"/><path d="M128.382 76.676h2.383l-1.324-7.411z"/><path stroke-width="1.0588248" stroke-linecap="round" stroke-linejoin="round" fill="none" stroke="#000" d="M128.382 76.676h2.383l-1.324-7.411zM125.735 102.882h-8.206M117.53 98.647h8.205M121.5 102.882v-4.235M64.059 82.5l41.823-11.647"/><path d="M105.618 70.059l6.353-.794-5.824 2.647z"/><path stroke-width="1.0588248" stroke-linecap="round" stroke-linejoin="round" fill="none" stroke="#000" d="M105.618 70.059l6.353-.794-5.824 2.647zM64.059 82.5L22.235 70.853"/><path d="M21.97 71.912l-5.823-2.647 6.353.794z"/><path stroke-width="1.0588248" stroke-linecap="round" stroke-linejoin="round" fill="none" stroke="#000" d="M21.97 71.912l-5.823-2.647 6.353.794zM50.294 76.676v-5.294M50.294 73.765l.265-1.324.53-.794.793-.265h.794"/></g></svg></center>

$$
\theta = 2arccos \frac{r-H}{r}
$$

$$
B = 2 \ \sqrt{H(2r-H)}
$$

$$
\omega = \frac{r^2}{2}(\theta - sin \theta)
$$

$$
\chi = r \theta
$$

$$
R = \frac{\omega}{\chi} = \frac{r}{2}\left( 1 - \frac{sin \theta}{\theta} \right)
$$
