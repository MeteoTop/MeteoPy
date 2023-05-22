<div align="center">
<!-- Title: -->
  <a href="https://gitee.com/MeteoTop/MeteoPy">
    <img src="./FigGallery/HEAD_log_1.png" height="100">
  </a>
  <h1><a href="https://gitee.com/MeteoTop/MeteoPy">MeteoPy</a> - Python</h1>
<!-- Labels: -->
  <!-- First row: -->
  <a href="https://gitee.com/MeteoTop/MeteoPy/blob/main/DEVELOPER.md">
    <img src="https://img.shields.io/badge/Contributions-Welcome-blue" height="20">
  </a>
  <a href="https://gitee.com/MeteoTop/MeteoPy/releases">
    <img src="https://img.shields.io/badge/MeteoPy-v0.0.2-brightgreen" height="20">
  </a>
  <a href="https://gitee.com/MeteoTop/MeteoPy/releases">
    <img src="https://img.shields.io/badge/Size-30KB-9cf" height="20">
  </a>
  <!-- Second row: -->
  <br>
  <a href="https://gitee.com/MeteoTop">
    <img src="https://img.shields.io/badge/Author-@MeteoTop-orange" height="20">
  </a>
  <a href="https://gitee.com/MeteoTop/MeteoPy">
    <img src="https://img.shields.io/badge/Last%20commit-2023--5--22-yellowgreen" height="20">
  </a>
  <!-- Short description: -->
  <h5>在此仓库中将存放一些我们在科研过程中实用的python脚本，主要针对大气科学学科</h5>
</div>

## 如何使用

请参照[MeteoPy如何安装](./DOWNLOAD.md)。

## 开发者

我们尝试将一些在大气科学学科科研中经常使用到的python程序封装成`函数`或者`类`，为气象事业做出自己的一份贡献。如果有志同道合的朋友，愿意为本开源函数库做出贡献，请仔细阅读[开发者说明](./DEVELOPER.md)。

## 依赖库说明

本函数库也依赖其他python库，详见[MeteoPy依赖库说明](./DEPENDENCE.md)。


## 函数库说明

此函数库中存有多个文件夹，初略可分为`功能文件夹`和`测试文件夹`。

### Test

此文件夹为函数测试文件夹，其中的脚本用于测试其他功能文件夹中的脚本。

+ 该文件夹下建有与各功能文件夹相对应的子测试文件夹，命名：`功能文件夹名Test`；
+ 子测试文件夹下，建有针对每个功能py文件的测试文件，命名：`功能文件名Test.ipynb`；
+ 测试文件为`jupyter notebook`格式，方便图文并茂显示每一个示例；

### Tools

此文件夹为工具文件夹，属于功能文件夹。存放一些工具类函数，如地图白化、Lambert投影的坐标刻度显示等等。在此测试文件夹内又将工具函数分为三类，FileTools.py、FunVarDefault.py、GraphTools.py。

+ `FileTools.py`：主要存放一些操作文件的工具函数；
+ `FunVarDefault.py`：存放一些在定义函数时，变量初始化的工具函数；
+ `GraphTools.py`：存放一些在绘制图表过程中使用到工具函数；

[工具文件夹介绍](./MeteoPy/Tools/README.md)

### MeteoDraw

此文件夹为气象绘图文件夹，属于功能文件夹。存放一些绘图函数，主要可能偏向气象学。

[绘图文件夹介绍](./MeteoPy/MeteoDraw/README.md)

### DataPro

此文件夹为数据处理文件夹，属于功能文件夹。存放一些数据处理的函数。

[数据处理文件夹介绍](./MeteoPy/DataPro/README.md)





