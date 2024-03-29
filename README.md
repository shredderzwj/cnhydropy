# cnhydropy
cnhydropy 中国水利水电工程设计计算程序集
China Water Conservancy and Hydropower Engineering Design and Calculation Program

本程序计算方法以及测试数据参考：

* 国家、行业相关规范；

* 相关技术书籍

* 《[水利水电工程设计计算程序集](http://www.slcxj.com)》 [使用说明书](http://slcxjyjs.realor.net:800/RTF/)

## 前言
本人毕业于河海大学水利水电学院农业水利工程系，求学期间就喜欢利用业余时间学习计算机编程，在课程设计和毕业设计的过程中，相关的计算就采用自编程序计算。特别是毕业设计，指导老师特别要求每个同学必须具有编程计算的能力，每个同学必须有自编计算程序。工作几年来，也写了一些程序，不过都是根据单个需求写的，没有进行系统的管理，不成体系，好多过一段时间都找不到了，再次使用时还得重新做。

《[水利水电工程设计计算程序集](http://www.slcxj.com)》（以下简称程序集）自1988年首版诞生以来，经过30年的发展，除了专家的审查与鉴定外，还经过了众多水利水电行业技术人员的实际工程的考验，进行了具体鉴定与审查，技术成果可靠。可以完成中小型工程的绝大部分常规计算，也可以用于大型工程的设计以及病险水库的安全鉴定和修复。目前已在40多个水利水电行业的甲级设计院以及各省、市、地区、县级水利水电设计单位推广使用，若干水利水电专业的高等院校已经将其用于教学和生产，受到广泛欢迎。程序集为收费软件，软件价格也并不便宜，因此，很多一线基层设计人员会听说过这个软件，但是由于自己的工作单位没有购买，没有机会使用，因为自己购买的话，可能仅会用到一小部分功能，很不划算。于是关于有没有程序集破解版的话题时不时的会出现在技术交流群中，使用盗版软件总是不好的，不但没有技术支持，而且破解软件里面有没有绑定木马也不得而知，总之，使用这样的破解软件无论是安全方面还是法律层面，都有很大的风险。

程序集之所以受到广大设计人员的欢迎，主要原因还是因为它大多数功能是专业的水利工作者开发，并且经过了众多水利水电行业技术人员的实际工程的考验，进行了具体鉴定与审查，技术成果可靠。但是经过试用，发现它并不“好用”，即使现在发行单位开发了视窗版。程序的打包、视窗等均使用的windows Xp时代的技术，与现代的windows 10兼容性并不好，程序的安装、授权、运行的过程中总是出现这样那样的问题，而且程序的输入也并不方便，灵活性很差。

现在互联网行业发展迅速，各种云计算的产生，H5以及Vue、React等各种web前端技术的发展，使web开发有了各种可能性。因此，可以设想，能不能把各个计算程序做成B/S架构的web应用，使用web技术绘制前端视窗，调用后台计算服务，最终实现水利的云计算。这样的话，只要你的电脑里面有一个现代的浏览器，不需要安装其他任何的软件，就可以计算了，甚至用手机也可以，结果还可以保存在数据库中，需要的时候可以随时调出来，并且可以基于现在强大的web前端实现程序的美观性和易用性，还可以在程序中加入一些内容服务，例如，可以加入参考书、引用规范等的连接，点击后可以快速查阅，这将省去很多查找资料的时间，对于新手设计人员不仅可以应用计算程序，还能学习计算原理，提升用户体验。另外，在商业化方面，此种架构会更灵活，在授权方面，可以采取注册会员制，会员可以选择单次使用、包月使用、包年使用等，甚至可以将程序集的每一个计算模块设置成一个商品，会员可以向在淘宝购物一样购买自己需要的那个模块，而不用像传统模式的必须要买整个程序集才能使用。

基于以上构想，这个代码仓库是水利云计算的开源后台核心计算库，是一个实验性的东西，使用Python语言实现，Python语言简单易学，功能强大，很适合工程人员学习使用。另外需说明的是，由于程序集功能过于繁多，不建议实现那些使用率不高、计算简单的功能，性价比太低，因此，仅实现那些使用率高并且计算复杂度高的功能。现免费开源给水利行业的编程爱好者共同研究学习！现在还没有实现许多功能，这需要时间积累，并且需要在不断的探索中改进。

愿此项目能够抛砖引玉，如果您对这个项目感兴趣，欢迎贡献您的一份力量，或者提供相关的需求建议也可，可以把您的想法发送至邮箱：shredderzwj@hotmail.com

程序集出版单位把相关程序的使用说明公开，大部分程序介绍了其主要计算方法，以及测试实例，鉴于程序集的权威性，可以利用这些资料，实现各个计算模块，程序集里面没有的功能，则需自己研发。如果本程序有侵权的地方请联系我删除。邮箱：shredderzwj@hotmail.com 。

最后的最后，由于本人水平有限，难免出现错误，欢迎批评指正。本人仅提供计算程序，不承担任何风险责任，若您使用程序所造成的一切损失均与本人无关。