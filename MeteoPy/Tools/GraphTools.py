# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author      :   nhno 
# @Time        :   2023/04/22 14:41:32
# @Description :   


def mark_inset(parent_axes, inset_axes, 
               loc1a : int = 2, 
               loc1b : int = 3, 
               loc2a : int = 1, 
               loc2b : int = 4, **kwargs):
    """放大地图中的某一区域，连接子图。根据inset_axes的extent范围，在parent_axes中
       框出指定区域，如果为兰伯特投影，则选择刚好包含extent的矩形区域

    Args:
        parent_axes (_type_): 放大后的ax
        inset_axes (_type_): 原来的ax
        loc1a (int, optional): 放大图连接的端点2，左上为1，顺时针. Defaults to 2.
        loc1b (int, optional): 原图连接的端点3. Defaults to 3.
        loc2a (int, optional): 放大图连接的端点1. Defaults to 1.
        loc2b (int, optional): 原图连接的端点4. Defaults to 4.

    注意：inset_axes需要用set_extent剪切区域，方便在parent_axes中找到对应区域
    默认值适用于上下分布的两个子图

    >>> mark_inset(ax, ax1, loc1a=2, loc1b=3, loc2a=1, loc2b=4, fc='none', ec='black', lw=1.75)
    """

    from mpl_toolkits.axes_grid1.inset_locator import TransformedBbox, BboxPatch, BboxConnector


    # # 根据inset_axes子图所设置的extent，在父图中圈出子图对应的矩形区域
    rect = TransformedBbox(inset_axes.viewLim, parent_axes.transData)
    pp = BboxPatch(rect, fill=False, **kwargs)
    parent_axes.add_patch(pp)

    p1 = BboxConnector(inset_axes.bbox, rect, loc1=loc1a, loc2=loc1b, **kwargs)
    inset_axes.add_patch(p1)
    p1.set_clip_on(False)
    p2 = BboxConnector(inset_axes.bbox, rect, loc1=loc2a, loc2=loc2b, **kwargs)
    inset_axes.add_patch(p2)
    p2.set_clip_on(False)

    return pp, p1, p2


class gridlines_tick():
    """
        在绘制地图中，需要添加经纬度坐标，此方法用于gridlines函数绘制的网格添加刻度线
        适用于LambertConformal(), PlateCarree().
        修改于https://zhajiman.github.io/post/cartopy_lambert/

        注意gridline中的参数draw_labels要调成False
    """

    def __init__(self, ax, xticks, yticks) -> None:
        """类参数初始化

        Args:
            ax (_type_): 绘图对象
            xtick (_type_): 横坐标刻度列表
            ytick (_type_): 纵坐标刻度列表
        """
        
        self.ax = ax
        self.xticks = xticks
        self.yticks = yticks

        # # 调用方法
        self.find_x_intersections()
        self.find_y_intersections()
        self.set_lambert_ticks()


    def find_x_intersections(self):
        """
            找出xticks对应的经线与下x轴的交点
            在data坐标下的位置和对应的ticklabel
        """
        
        import numpy as np
        import cartopy.crs as ccrs
        import shapely.geometry as sgeom
        from cartopy.mpl.ticker import LongitudeFormatter


        # 获取地图的矩形边界和最大的经纬度范围.
        x0, x1, y0, y1 = self.ax.get_extent()
        lon0, lon1, lat0, lat1 = self.ax.get_extent(ccrs.PlateCarree())
        xaxis = sgeom.LineString([(x0, y0), (x1, y0)])
        # 仅选取能落入地图范围内的ticks.
        lon_ticks = [tick for tick in self.xticks if tick >= lon0 and tick <= lon1]

        # 每条经线有nstep个点.
        nstep = 50
        self.xlocs = []
        self.xticklabels = []
        for tick in lon_ticks:
            lon_line = sgeom.LineString(
                self.ax.projection.transform_points(
                        ccrs.Geodetic(),
                        np.full(nstep, tick),
                        np.linspace(lat0, lat1, nstep)
                    )[:, :2]
            )
            # 如果经线与x轴有交点,获取其位置.
            if xaxis.intersects(lon_line):
                point = xaxis.intersection(lon_line)
                self.xlocs.append(point.x)
                self.xticklabels.append(tick)
            else:
                continue

        # 用formatter添上度数和东西标识.
        formatter = LongitudeFormatter()
        self.xticklabels = [formatter(label) for label in self.xticklabels]


    def find_y_intersections(self):
        '''
            找出yticks对应的纬线与左y轴的交点
            在data坐标下的位置和对应的ticklabel
        '''
        
        import numpy as np
        import cartopy.crs as ccrs
        import shapely.geometry as sgeom
        from cartopy.mpl.ticker import LatitudeFormatter
        

        x0, x1, y0, y1 = self.ax.get_extent()
        lon0, lon1, lat0, lat1 = self.ax.get_extent(ccrs.PlateCarree())
        yaxis = sgeom.LineString([(x0, y0), (x0, y1)])
        lat_ticks = [tick for tick in self.yticks if tick >= lat0 and tick <= lat1]

        nstep = 50
        self.ylocs = []
        self.yticklabels = []
        for tick in lat_ticks:
            # 注意这里与find_x_intersections的不同.
            lat_line = sgeom.LineString(
                self.ax.projection.transform_points(
                        ccrs.Geodetic(),
                        np.linspace(lon0, lon1, nstep),
                        np.full(nstep, tick)
                    )[:, :2]
            )
            if yaxis.intersects(lat_line):
                point = yaxis.intersection(lat_line)
                self.ylocs.append(point.y)
                self.yticklabels.append(tick)
            else:
                continue

        formatter = LatitudeFormatter()
        self.yticklabels = [formatter(label) for label in self.yticklabels]


    def set_lambert_ticks(self):
        '''
            给一个LambertConformal投影的GeoAxes在下x轴与左y轴上添加ticks.
            要求地图边界是矩形的,即ax需要提前被set_extent方法截取成矩形.否则可能会出现错误.
        '''
        # 设置x轴
        self.ax.set_xticks(self.xlocs)
        self.ax.set_xticklabels(self.xticklabels)
        # 设置y轴
        self.ax.set_yticks(self.ylocs)
        self.ax.set_yticklabels(self.yticklabels)


def adjust_sub_axes(ax_parant, ax_sub, shrink : float = 0.15):
    """将ax_sub调整到ax_parant的左下角，并按shrink进行缩放
       主要可以用于绘制中国南海小地图，南海小地图范围可选[105, 123, 2, 23]
       参考：https://blog.csdn.net/weixin_44237337/article/details/123557098

    Args:
        ax_parant (_type_): 父图绘图对象
        ax (_type_): 目标子图对象
        shrink (float, optional): 目标子图缩放大小. Defaults to 0.2.
        
    >>> map_proj = ccrs.LambertConformal(
                    central_longitude=105, standard_parallels=(25, 47)
                    )
    >>> # # 创建空白画布
    >>> fig = plt.figure(figsize=(8, 5))
    >>> # # 父图
    >>> ax_parant = fig.add_subplot(1, 1, 1, projection=map_proj)
    >>> # # 创建绘图实例
    >>> draw = Draw_map()
    >>> draw.comunity_maps(ax_parant, extent=[80, 130, 15, 55], xticks=np.arange(80, 130.1, 10),
                           yticks=np.arange(5, 45.1, 10), cnmap={'country':'中华人民共和国'})
 
    >>> ax_sub = fig.add_subplot(1, 1, 1, projection=map_proj)
    >>> draw.comunity_maps(ax_sub, extent=[105, 123, 2, 23], tick=[0, 0], cnmap={'country':'中华人民共和国'})
    >>> adjust_sub_axes(ax_parant, ax_sub, 0.15)
    """
    
    import matplotlib.transforms as mtransforms

    bbox_parent = ax_parant.get_position()  # 获取父图在fig中的位置
    bbox_sub = ax_sub.get_position()  # 获取目标子图在fig中的位置

    ratio = bbox_parent.width / bbox_sub.width  # 图片父图与目标子图的比例
    wnew = bbox_sub.width * ratio * shrink  # 缩放后子图的宽度
    hnew = bbox_sub.height * ratio * shrink  # 缩放后子图的高度

    bbox_new = mtransforms.Bbox.from_extents(
        bbox_parent.x1 - wnew, bbox_parent.y0,
        bbox_parent.x1, bbox_parent.y0 + hnew
    )  # 根据缩放后子图的宽度、高度，以及父图的位置信息，重新指定子图位置为父图左下角
    ax_sub.set_position(bbox_new)  # 将目标子图移动至父图的左下角


def box_select_rectangular(ax, 
                           extent : list, 
                           smooth : int = None,
                           type : dict = {'color':'black', 'linewidth':1, 'linestyle':'-'}):
    """在地图中根据extent框出该矩形区域，PlateCarree()为矩形，LambertConformal()为扇形，
       但如果关闭平滑系数smooth,则均为矩形，默认关闭，框出刚好包含extent的矩形区域；
       如果在兰伯特投影时想画扇形，则设置一个平滑系数；
       参考：https://zhajiman.github.io/post/cartopy_lambert/

    Args:
        ax (_type_): 绘图对象
        extent (list): 矩形区域范围[经度左, 经度右, 维度下, 维度上]
        smooth (int, optional): 线条平滑系数（次数）. Defaults to 20.
        type (dict, optional): 设置plot线条类型. Defaults to {'color':'black', 'linewidth':1, 'linestyle':'-'}.
    """

    import cartopy.crs as ccrs
    import matplotlib.path as mpath
    import matplotlib.pyplot as plt
    from MeteoPy import dict_default
    from mpl_toolkits.axes_grid1.inset_locator import TransformedBbox, BboxPatch

    
    # # 处理type默认值问题
    type_default = {'color':'black', 'linewidth':1, 'linestyle':'-'}
    type = dict_default(type, type_default)
    print('type=', end='')
    print(type)

    if smooth:
        rect = mpath.Path([
            [extent[0], extent[2]],
            [extent[0], extent[3]],
            [extent[1], extent[3]],
            [extent[1], extent[2]],
            [extent[0], extent[2]]
        ]).interpolated(smooth)  # 平滑插值，区别主要在绘制兰伯特投影的时候，有了这个，绘制的区域为扇形
        line = rect.vertices
        ax.plot(line[:, 0], line[:, 1], color=type['color'], linewidth=type['linewidth'], 
                linestyle=type['linestyle'], transform=ccrs.PlateCarree())

    else:
        # 创建一个画布和子图，主要为了使用set_extent剪切区域，方便TransformedBbox获取
        # 完成框选之后，删除画布
        fig1 = plt.figure()
        ax1 = fig1.add_subplot(1, 1, 1, projection=ax.projection)
        ax1.set_extent(extent, crs=ccrs.PlateCarree())

        rect = TransformedBbox(ax1.viewLim, ax.transData)
        pp = BboxPatch(rect, fill=False, color=type['color'], linewidth=type['linewidth'], 
                       linestyle=type['linestyle'])
        ax.add_patch(pp)
        plt.close()


def shp2clip(originfig, ax, 
             shpfile : str, 
             fieldVals : list, 
             vcplot : bool = False,
             clabel : list = None):
    """地图掩膜

    Args:
        originfig (_type_): 掩膜对象，cotour_f返回的cs
        ax (_type_): 绘图对象
        shpfile (str): 用来掩膜的地图文件shp
        fieldVals (list): 地图文件shp中能唯一确定想要保留区域的识别符（可以是任意且唯一确定的）
                           可以是一个，或多个(表示想要保留的对象不止一个)
                           [在shp文件中标识符对应的索引号, [标识符]]
        vcplot (bool, optional): 是否对风矢量进行白化. default. False
        clabel (list, optional): ax.clabel()返回的对象，对等值线标签进行白化. default. None

    Returns:
        _type_: _description_
    """

    import shapefile
    from matplotlib.path import Path
    from collections import Iterable
    from matplotlib.patches import PathPatch
    from shapely.geometry import Point as ShapelyPoint
    from shapely.geometry import Polygon as ShapelyPolygon


    sf = shapefile.Reader(shpfile)
    vertices = []
    codes = []
    for shape_rec in sf.shapeRecords():
        if shape_rec.record[fieldVals[0]] in fieldVals[1]:  # 注意这里需要指定你的字段的索引号，我的是第3个字段
            pts = shape_rec.shape.points
            prt = list(shape_rec.shape.parts) + [len(pts)]
            for i in range(len(prt) - 1):
                for j in range(prt[i], prt[i + 1]):
                    vertices.append((pts[j][0], pts[j][1]))
                codes += [Path.MOVETO]
                codes += [Path.LINETO] * (prt[i + 1] - prt[i] - 2)
                codes += [Path.CLOSEPOLY]
            clip = Path(vertices, codes)
            clip = PathPatch(clip, transform=ax.transData)

    for contour in originfig.collections:
        contour.set_clip_path(clip)
    
    # # 白化风矢量
    if vcplot:
        if isinstance(originfig, Iterable):
            for ivec in originfig:
                ivec.set_clip_path(clip)
        else:
            originfig.set_clip_path(clip)
    else:
        for contour in originfig.collections:
            contour.set_clip_path(clip)

    # # 白化等值线标签
    if  clabel:
        clip_map_shapely = ShapelyPolygon(vertices)
        for text_object in clabel:
            if not clip_map_shapely.contains(ShapelyPoint(text_object.get_position())):
                text_object.set_visible(False)  

    return clip


def LU_MODIS20():
    """MODIS-20种土地利用类型 
       绘制的土地类型、标签与对应色标
       引自: https://github.com/blaylockbk/Ute_WRF/blob/master/functions/landuse_colormap.py
    Returns:
        cm: 颜色卡
        labels: 土地利用类型标签

    >>> # 调用颜色和标签
    >>> cm, labels = LU_MODIS20()
    >>> im = self.ax1.pcolormesh(lons, lats, landuse, transform=ccrs.PlateCarree()
    >>>                          vmin=1, vmax=len(labels) + 1, cmap=cm)  # vmin和vmax必不可少，与后面的cbar.set_ticks相对应
    >>> # 添加色标
    >>> position = self.fig.add_axes([0.90, 0.13, 0.018, 0.31])  # 坐标＋长宽
    >>> cbar = self.fig.colorbar(im, shrink=1, cax=position, orientation='vertical')
    >>> cbar.set_ticks(np.arange(1.5, len(labels) + 1))  # 使标签标注在每个颜色中间
    >>> cbar.ax.set_yticklabels(labels)
    """

    import numpy as np
    from matplotlib.colors import ListedColormap


    C = np.array([
        [0,.4,0],           #  1 Evergreen Needleleaf Forest
        [0,.4,.2],          #  2 Evergreen Broadleaf Forest    
        [.2,.8,.2],         #  3 Deciduous Needleleaf Forest
        [.2,.8,.4],         #  4 Deciduous Broadleaf Forest
        [.2,.6,.2],         #  5 Mixed Forests
        [.3,.7,0],          #  6 Closed Shrublands
        [.82,.41,.12],      #  7 Open Shurblands
        [.74,.71,.41],      #  8 Woody Savannas
        [1,.84,.0],         #  9 Savannas
        [0,1,0],            #  10 Grasslands
        [0,1,1],            #  11 Permanant Wetlands
        [1,1,0],            #  12 Croplands
        [1,0,0],            #  13 Urban and Built-up
        [.7,.9,.3],         #  14 Cropland/Natual Vegation Mosaic
        [1,1,1],            #  15 Snow and Ice
        [.914,.914,.7],     #  16 Barren or Sparsely Vegetated
        [0,0,.88],          #  17 Water
        [.86,.08,.23],      #  18 Wooded Tundra
        [.97,.5,.31],       #  19 Mixed Tundra
        [.91,.59,.48]])     #  20 Barren Tundra

    cm = ListedColormap(C)
    
    labels = ['Evergreen Needleleaf Forest',
              'Evergreen Broadleaf Forest',
              'Deciduous Needleleaf Forest',
              'Deciduous Broadleaf Forest',
              'Mixed Forests',
              'Closed Shrublands',
              'Open Shrublands',
              'Woody Savannas',
              'Savannas',
              'Grasslands',
              'Permanent Wetlands',
              'Croplands',
              'Urban and Built-Up',
              'Cropland/Natural Vegetation Mosaic',
              'Snow and Ice',
              'Barren or Sparsely Vegetated',
              'Water',
              'Wooded Tundra',
              'Mixed Tundra',
              'Barren Tundra']
    
    return cm, labels


def LU_MODIS21():
    """MODIS-21种土地利用类型 
       绘制的土地类型、标签与对应色标

    Returns:
        cm: 颜色卡
        labels: 土地利用类型标签
    
    >>> # 调用颜色和标签
    >>> cm, labels = LU_MODIS21()
    >>> im = self.ax1.pcolormesh(lons, lats, landuse, transform=ccrs.PlateCarree()
    >>>                          vmin=1, vmax=len(labels) + 1, cmap=cm)  # vmin和vmax必不可少，与后面的cbar.set_ticks相对应
    >>> # 添加色标
    >>> position = self.fig.add_axes([0.90, 0.13, 0.018, 0.31])  # 坐标＋长宽
    >>> cbar = self.fig.colorbar(im, shrink=1, cax=position, orientation='vertical')
    >>> cbar.set_ticks(np.arange(1.5, len(labels) + 1))  # 使标签标注在每个颜色中间
    >>> cbar.ax.set_yticklabels(labels)
    """

    import numpy as np
    from matplotlib.colors import ListedColormap


    C = np.array([
        [0, .4, 0],         # 1 Evergreen Needleleaf Forest
        [0, .4, .2],        # 2 Evergreen Broadleaf Forest
        [.2, .8, .2],       # 3 Deciduous Needleleaf Forest
        [.2, .8, .4],       # 4 Deciduous Broadleaf Forest
        [.2, .6, .2],       # 5 Mixed Forests
        [.3, .7, 0],        # 6 Closed Shrublands
        [.82, .41, .12],    # 7 Open Shurblands
        [.74, .71, .41],    # 8 Woody Savannas
        [1, .84, .0],       # 9 Savannas
        [0, 1, 0],          # 10 Grasslands
        [0, 1, 1],          # 11 Permanant Wetlands
        [1, 1, 0],          # 12 Croplands
        [1, 0, 0],          # 13 Urban and Built-up
        [.7, .9, .3],       # 14 Cropland/Natual Vegation Mosaic
        [1, 1, 1],          # 15 Snow and Ice
        [.914, .914, .7],   # 16 Barren or Sparsely Vegetated
        [.5, .7, 1],        # 17 Water (like oceans)
        [.86, .08, .23],    # 18 Wooded Tundra
        [.97, .5, .31],     # 19 Mixed Tundra
        [.91, .59, .48],    # 20 Barren Tundra
        [0, 0, .88]])       # 21 Lake

    cm = ListedColormap(C)

    labels = ['Evergreen Needleleaf Forest',
              'Evergreen Broadleaf Forest',
              'Deciduous Needleleaf Forest',
              'Deciduous Broadleaf Forest',
              'Mixed Forests',
              'Closed Shrublands',
              'Open Shrublands',
              'Woody Savannas',
              'Savannas',
              'Grasslands',
              'Permanent Wetlands',
              'Croplands',
              'Urban and Built-Up',
              'Cropland/Natural Vegetation Mosaic',
              'Snow and Ice',
              'Barren or Sparsely Vegetated',
              'Water',
              'Wooded Tundra',
              'Mixed Tundra',
              'Barren Tundra',
              'Lake']

    return cm, labels


def LU_USGS24():
    """MODIS-24种土地利用类型 
       绘制的土地类型、标签与对应色标
    
    Returns:
        cm: 颜色卡
        labels: 土地利用类型标签

    >>> # 调用颜色和标签
    >>> cm, labels = LU_MODIS24()
    >>> im = self.ax1.pcolormesh(lons, lats, landuse, transform=ccrs.PlateCarree()
    >>>                          vmin=1, vmax=len(labels) + 1, cmap=cm)  # vmin和vmax必不可少，与后面的cbar.set_ticks相对应
    >>> # 添加色标
    >>> position = self.fig.add_axes([0.90, 0.13, 0.018, 0.31])  # 坐标＋长宽
    >>> cbar = self.fig.colorbar(im, shrink=1, cax=position, orientation='vertical')
    >>> cbar.set_ticks(np.arange(1.5, len(labels) + 1))  # 使标签标注在每个颜色中间
    >>> cbar.ax.set_yticklabels(labels)
    """

    import numpy as np
    from matplotlib.colors import ListedColormap

    
    C = np.array([
        [1,0,0],            #  1 Urban and Built-up Land
        [1,1,0],            #  2 Dryland Cropland and Pasture
        [1,1,.2],           #  3 Irrigated Cropland and Pasture
        [1,1,.3],           #  4 Mixed Dryland/Irrigated Cropland and Pasture
        [.7,.9,.3],         #  5 Cropland/Grassland Mosaic
        [.7,.9,.3],         #  6 Cropland/Woodland Mosaic
        [0,1,0],            #  7 Grassland
        [.3,.7,0],          #  8 Shrubland
        [.82,.41,.12],      #  9 Mixed Shrubland/Grassland
        [1,.84,.0],         #  10 Savanna
        [.2,.8,.4],         #  11 Deciduous Broadleaf Forest
        [.2,.8,.2],         #  12 Deciduous Needleleaf Forest
        [0,.4,.2],          #  13 Evergreen Broadleaf Forest
        [0,.4,0],           #  14 Evergreen Needleleaf Forest 
        [.2,.6,.2],         #  15 Mixed Forests
        [0,0,.88],          #  16 Water Bodies
        [0,1,1],            #  17 Herbaceous Wetlands
        [.2,1,1],           #  18 Wooden Wetlands
        [.914,.914,.7],     #  19 Barren or Sparsely Vegetated
        [.86,.08,.23],      #  20 Herbaceous Tundraa
        [.86,.08,.23],      #  21 Wooded Tundra
        [.97,.5,.31],       #  22 Mixed Tundra
        [.91,.59,.48],      #  23 Barren Tundra
        [1,1,1]             #  24 Snow and Ice
        ])
    
    cm = ListedColormap(C)
    
    labels = ['Urban and Built-up Land',
              'Dryland Cropland and Pasture',
              'Irrigated Cropland and Pasture',
              'Mixed Dryland/Irrigated Cropland and Pasture',
              'Cropland/Grassland Mosaic',
              'Cropland/Woodland Mosaic',
              'Grassland',
              'Shrubland',
              'Mixed Shrubland/Grassland',
              'Savanna',
              'Deciduous Broadleaf Forest',
              'Deciduous Needleleaf Forest',
              'Evergreen Broadleaf',
              'Evergreen Needleleaf',
              'Mixed Forest',
              'Water Bodies',
              'Herbaceous Wetland',
              'Wooden Wetland',
              'Barren or Sparsely Vegetated',
              'Herbaceous Tundra',
              'Wooded Tundra',
              'Mixed Tundra',
              'Bare Ground Tundra',
              'Snow or Ice']
    
    return cm, labels   
    

def image_to_video(image_path : str, 
                   media_path : str, 
                   fps : int = 2):
    """图片合成视频

    Args:
        image_path (str): 系列图片存放路径(父文件夹地址)，末尾不带\
        media_path (str): 合成的视频存放路径，注意指定视频格式.mp4
        fps (int, optional): 每秒显示的图片数. Defaults to 2.

    Attention:
        1. 图片路径和视频路径中不得含有中文；
        2. 图片dpi不能太高，否则合成视频的太大；
        3. 图片命名建议用表示先后顺序的数字；
    """


    import os
    import cv2  # python非标准库，pip install opencv-python 多媒体处理
    from PIL import Image, ImageSequence  # python非标准库，pip install pillow，图像处理

    # 获取图片路径下面的所有图片名称
    image_names = os.listdir(image_path)
    # 对提取到的图片名称进行排序
    image_names.sort(key=lambda n: int(n[:-4]))
    # 设置写入格式
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    
    # 读取第一个图片获取大小尺寸，因为需要转换成视频的图片大小尺寸是一样的
    image = Image.open(image_path + '\\' + image_names[0])
    # 初始化媒体写入对象
    media_writer = cv2.VideoWriter(media_path, fourcc, fps, image.size)
    # 遍历图片，将每张图片加入视频当中
    for image_name in image_names:
        im = cv2.imread(os.path.join(image_path, image_name))
        media_writer.write(im)
        print(image_name, '合并完成！')
    # 释放媒体写入对象
    media_writer.release()
    print('无声视频写入完成！')


def picture_to_gif(image_path : str, 
                   gif_path : str, 
                   picture_type : str, 
                   freq : float = 0.2):
    """图片合成gif动图

    Args:
        image_path (str): 图片路径, 文件夹路径末尾不带\
        gif_path (str): 合成.gif保存路径, 需要带上文件名
        picture_type (str): 图片格式，带.号
        freq (float): 显示频率，每张图片显示的持续时间. Defaults to 0.2.
    """
    

    import os
    import imageio

    # 获取图片路径下面的所有图片名称
    image_names = os.listdir(image_path)
    # 只获取指定格式图片
    image_names = list(filter(lambda x: x[-4:] == picture_type, image_names))
    # 对提取到的图片名称进行排序
    image_names.sort(key=lambda n: int(n[:-4]))

    imglist = []
    for i in image_names:
        imglist.append(imageio.imread(image_path + '\\' + i))

    imageio.mimsave(gif_path, imglist, 'GIF', duration=freq)


def compress_gif(gif_file : str, 
                 new_gif_file : str, 
                 rp : int):
    """压缩gif动图

    Args:
        gif_file (str): 欲压缩gif文件地址
        new_gif_file (str): 压缩后的gif存放地址
        rp (int): 自定义压缩后的图片尺寸rp*rp
    """
    
    
    import imageio
    from PIL import Image, ImageSequence  # python非标准库，pip install pillow，图像处理

    # 图片缓存空间
    image_list = []
    # 读取gif图片
    im = Image.open(gif_file)
    # 提取每一帧，并对其进行压缩，存入image_list
    for frame in ImageSequence.Iterator(im):
        frame = frame.convert('RGB')
        if max(frame.size[0], frame.size[1]) > rp:
            frame.thumbnail((rp, rp))
        image_list.append(frame)

    # 计算帧之间的频率，间隔毫秒
    duration = im.info['duration'] / 1000

    # 读取image_list合并成gif
    imageio.mimsave(new_gif_file, image_list, duration=duration)











