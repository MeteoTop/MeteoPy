# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author      :   nhno 
# @Time        :   2023/04/07 16:39:47
# @Description :   


class Draw_map():

    def __init__(self):
        pass


    def comunity_maps(self, ax, 
                      extent : list = None, 
                      xticks : list = None, 
                      yticks : list = None, 
                      basemape : dict = None,
                      cnmap : dict = None, 
                      title : str = None, 
                      tag : str = None, 
                      tick : list = [1, 1], 
                      shp_file : str = None):
        """设置地图通用部分

        Args:
            ax (_type_): 绘图对象
            extent (list, optional): 地图范围. Defaults to None.
            xticks (list, optional): x坐标刻度显示列表. Defaults to None.
            yticks (list, optional): y坐标刻度显示列表. Defaults to None.
            basemap (list, optional): 绘制基础地图，仅海岸线、河流、湖泊、海洋、陆地;
            cnmap (dict, optional): 绘制中国区域地图. Defaults to None. 
                    {'country':'中华人民共和国','province':'四川省', 'city':'达州市', 'district':'达川区', 'level':'区', 'inline':True}, 值可以为列表
            title (str, optional): 图片标题. Defaults to None.
            tag (str, optional): 图片标签(a). Defaults to None.
            tick (list, optional): 是否显示左侧和底部坐标. Defaults to [1, 1].
            shp_file (str, optional): shp文件地址. Defaults to [1, 1].
        """

        # # 导入函数库
        import os
        import numpy as np
        import cnmaps as cnm
        import cartopy.crs as ccrs
        import cartopy.feature as cfeature
        from matplotlib.image import imread
        from cartopy.io.shapereader import Reader
        from MeteoPy import gridlines_tick
        from MeteoPy import dict_default

        # # 处理cnmap默认值问题
        cnmap_default = {'country':None, 'province':None, 'city':None, 'district':None, 
                         'level':None, 'inline':True, 'linewidth':0.8}
        if isinstance(cnmap, dict):
            cnmap = dict_default(cnmap, cnmap_default)
        print('cnmap=', end='')
        print(cnmap)
        # # basemap中的值，与cfeature.的对应关系
        basemap_index = {'海岸线':cfeature.COASTLINE,
                         '河流':cfeature.RIVERS,
                         '湖泊':cfeature.LAKES,
                         '海洋':cfeature.OCEAN,
                         '陆地':cfeature.LAND,
                         '国界':cfeature.BORDERS  # 有中国时，不建议使用，缺少部分地区
                         }

        # 投影区域设置
        if extent:
            ax.set_extent(extent, crs=ccrs.PlateCarree())  # 调整地图经纬度范围,crs很重要

        # # 根据shp文件绘制地图地图
        if shp_file:
            provinces1 = cfeature.ShapelyFeature(
                Reader(shp_file).geometries(),
                ccrs.PlateCarree(), edgecolor='k',
                facecolor='none'
            )
            ax.add_feature(provinces1, linewidth=0.8, zorder=2)

        # # 基础地图则添加海岸线
        if isinstance(basemape, list):
            # # 搜索basemape，查看是否有字典，即是否有带.tif的地形数据
            for i in basemape:
                if isinstance(i, dict):
                    # --加载高分辨率地形
                    ax.imshow(
                        imread(i['地形']),
                        origin='upper', transform=ccrs.PlateCarree(),
                        extent=[-180, 180, -90, 90]
                    )
                    basemape.remove(i)

            if '地形' in basemape:
                ax.stock_img()   # 粗地形
                basemape.remove('地形')
            # # 添加背景
            for i in basemape:
                ax.add_feature(basemap_index[i], lw=0.8)
         
        # # 设置中国行政区域
        if isinstance(cnmap, dict):
            # # 先画中国国界
            if cnmap['country']:
                map = cnm.get_adm_maps(country='中华人民共和国')
                cnm.draw_maps(map, ax, linewidth=cnmap['linewidth'], color='k')
                
            # # 添加行政边界
            if isinstance(cnmap['province'], list):  # 如果cnmap['province']为列表
                temp_maps = []  # 存放各个省
                for i in cnmap['province']:
                    temp_map = cnm.get_adm_maps(province=i, only_polygon=True, record='first')
                    temp_maps.append(temp_map)
                map = temp_maps[0]
                for i in range(1, len(temp_maps)):
                    map = map + temp_maps[i]
                cnm.draw_map(map, ax, linewidth=cnmap['linewidth'], color='k')

                if cnmap['inline']:  # 保留省与省的界限
                    for i in cnmap['province']: 
                        map = cnm.get_adm_maps(province=i, city=cnmap['city'], 
                                               district=cnmap['district'], level=cnmap['level'])
                        cnm.draw_maps(map, ax, linewidth=cnmap['linewidth'], color='k')

            elif cnmap['province']:
                map = cnm.get_adm_maps(province=cnmap['province'], city=cnmap['city'], 
                                       district=cnmap['district'], level=cnmap['level'])
                cnm.draw_maps(map, ax, linewidth=cnmap['linewidth'], color='k')

            else:
                map = cnm.get_adm_maps(province=cnmap['province'], city=cnmap['city'], 
                                       district=cnmap['district'], level=cnmap['level'])
                cnm.draw_maps(map, ax, linewidth=cnmap['linewidth'], color='k')
        
        # # 设置经纬度刻度
        if (isinstance(xticks, np.ndarray) and isinstance(yticks, np.ndarray)) or \
            (isinstance(xticks, list) and isinstance(yticks, list)):
            # # 设置网格
            gl = ax.gridlines(xlocs=xticks, ylocs=yticks, x_inline=False, y_inline=False, 
                              draw_labels=False, linestyle="dotted", 
                              linewidth=1, alpha=0.4)
            # 关闭上面和右边的经纬度显示
            gl.top_labels = False  #关闭上部经纬标签
            gl.right_labels = False # 关闭右侧经纬度标签
            gl.rotate_labels = None  # 关闭坐标旋转
            # # 设置坐标刻度，最好是使用了set_extent对地图进行了裁剪
            gridlines_tick(ax, xticks, yticks)

            if tick[0] == 0:
                ax.set_yticklabels([])
            if tick[1] == 0:
                ax.set_xticklabels([])
        else:
            # # 设置网格
            gl = ax.gridlines(x_inline=False, y_inline=False, draw_labels=True, linestyle="dotted", 
                              linewidth=1, alpha=0.4)
            # 关闭上面和右边的经纬度显示
            gl.top_labels = False  #关闭上部经纬标签
            gl.right_labels = False  # 关闭右侧经纬度标签
            gl.rotate_labels = None  # 关闭坐标旋转

            if tick[0] == 0:
                gl.left_labels = False  # 关闭左边经纬度标签
            if tick[1] == 0:
                gl.bottom_labels = False  # 关闭下部经纬度标签

        # 设置刻度字体大小
        ax.tick_params(labelsize=12)

        # # 设置标题
        if title:
            ax.set_title(title, fontsize=12)
        # # 设置标签
        if tag:
            ax.text(0.017, 0.955, tag, transform=ax.transAxes, backgroundcolor='white', 
                    fontdict={'size':10})


    def draw_wind(self, ax, 
                  lon : list, 
                  lat : list, 
                  u : list, 
                  v : list, 
                  width : float = 0.005,
                  scale : float = 60,
                  sep : int = 4):
        """绘制风场图

        Args:
            ax (_type_): 绘图对象
            lon (list): 经度, list或者numpy
            lat (list): 纬度, list或者numpy
            u (list): u风速, list或者numpy
            v (list): v风速, list或者numpy
            width (float, optional): 值越大箭头/长度越大. Defaults to 0.005.
            scale (float, optional): 值越小箭头越长. Defaults to 60.
            sep (int, optional): 绘图间隔. Defaults to 4.
        """

        import numpy as np
        import cartopy.crs as ccrs

        lon, lat = np.array(lon), np.array(lat)
        u, v = np.array(u), np.array(v)
        # # 绘图
        q = ax.quiver(lon[::sep, ::sep], lat[::sep, ::sep], u[::sep, ::sep], v[::sep, ::sep], 
                      width=width, scale=scale, transform=ccrs.PlateCarree())  # scale越小箭头越长，width越大箭头/长度越大
        # # 风速标签
        ax.quiverkey(q, 0.88, 1.03, 4, '4m/s', coordinates='axes', labelpos='E', fontproperties={'size':10})
        ax.set_title(' ')


    def draw_contour_f(self, fig, ax, 
                       lon : list, 
                       lat : list, 
                       var : list, 
                       type : dict):
        """绘制等值线or填色图or打点图

        Args:
            fig (_type_): 画布
            ax (_type_): 绘图对象
            lon (list): 经度
            lat (list): 纬度
            var (list): 需要绘制的物理量
            type (dict): 绘图参数设置
               .Defaults to {'contourf':{'levels':None, 填色图显示范围
                                        'hatches':None, 画打点图使用
                                        'cmap':None, 填色图色标颜色
                                        'cbar':None}, 是否显示色标，[position, 'vertical', 'm/s']
                            'contour':{'levels':None, 等值线图显示范围
                                        'colors':'k', 等值线颜色，默认黑色
                                        'linewidths':1, 等值线粗细，默认1
                                        'clabel':None}, 是否标注等值线数值，[显示间隔, 显示格式],eg.[2, '%.5f']
                            '南海':{'extent':[105, 123, 2, 23], 'shrink':0.15}}
        """

        import cartopy.crs as ccrs
        from MeteoPy import dict_default
        from MeteoPy import adjust_sub_axes

        # # 处理type默认值问题
        type_default = {'contourf':{'levels':None, 'hatches':None, 'cmap':None, 'cbar':None},
                        'contour':{'levels':None, 'colors':'k', 'linewidths':1, 'clabel':None}, 
                        '南海':{'extent':[105, 123, 2, 23], 'shrink':0.15}}
        for key in type_default.keys():
            try:
                if isinstance(type[key], dict):
                    type[key] = dict_default(type[key], type_default[key])
            except KeyError:
                type[key] = None
        print('type=', end='')
        print(type)

        # # 判断是否绘制南海小地图
        if isinstance(type['南海'], dict):
            ax_sub = fig.add_subplot(1, 1, 1, projection=ax.projection)
            self.comunity_maps(ax_sub, extent=[105, 123, 2, 23], tick=[0, 0], cnmap={'country':'中华人民共和国'})
            # # 调整南海小地图位置，到左下角
            adjust_sub_axes(ax, ax_sub, type['南海']['shrink'])

        # # 绘图
        if isinstance(type['contourf'], dict):
            if type['contourf']['hatches']:  # # 打点图
                ax.contourf(lon, lat, var, levels=type['contourf']['levels'], zorder=1,
                            hatches=type['contourf']['hatches'], colors='none', 
                            transform=ccrs.PlateCarree())
                
                if isinstance(type['南海'], dict):
                    ax_sub.contourf(lon, lat, var, levels=type['contourf']['levels'], zorder=1,
                                    hatches=type['contourf']['hatches'], colors='none', 
                                    transform=ccrs.PlateCarree())

            else:
                cs = ax.contourf(lon, lat, var, levels=type['contourf']['levels'], cmap=type['contourf']['cmap'], 
                                 extend='both', transform=ccrs.PlateCarree())
                
                if isinstance(type['南海'], dict):
                    ax_sub.contourf(lon, lat, var, levels=type['contourf']['levels'], cmap=type['contourf']['cmap'], 
                                    extend='both', transform=ccrs.PlateCarree())
            
            if type['contourf']['cbar']:
                # # 添加色标
                position = fig.add_axes(type['contourf']['cbar'][0])  # 坐标＋长宽
                cbar = fig.colorbar(cs, shrink=1, cax=position, orientation=type['contourf']['cbar'][1])
                cbar.ax.tick_params(labelsize=12)  # 设置色标刻度字体大小
                cbar.set_label(type['contourf']['cbar'][2], fontsize=14)    # 单位

        if isinstance(type['contour'], dict):
            css = ax.contour(lon, lat, var, levels=type['contour']['levels'], linewidths=type['contour']['linewidths'], 
                             colors=type['contour']['colors'], transform=ccrs.PlateCarree())
            
            if isinstance(type['南海'], dict):
                ax_sub.contour(lon, lat, var, levels=type['contour']['levels'], linewidths=type['contour']['linewidths'], 
                               colors=type['contour']['colors'], transform=ccrs.PlateCarree())
                
            if type['contour']['clabel']:
                ax.clabel(css, css.levels[::type['contour']['clabel'][0]], inline=True, 
                          fmt=type['contour']['clabel'][1], fontsize=10)


def draw_time_box(ax, 
                  data : list, 
                  time : list, 
                  ticks : list, 
                  time_step : str, 
                  start_time : str = False, 
                  font : dict = None):
    """绘制箱线图，对某一时间序列数据指定时间间隔绘制箱线图

    Args:
        ax (_type_): 传入的绘图对象，即绘图框;
        data (list): 绘图数据，建议使用list或者numpy格式，一维数组;
        time (list): 绘图数据对应时间，建议使用list或者numpy格式，且时间本身需转化时间格式datatime;
        ticks (list): 指定坐标轴上进行显示的刻度（索引）;
        time_step (str): 指定绘图时间间隔时间间隔，即将多长时间的数据画一个箱线图, https://pandas.pydata.org/docs/user_guide/timeseries.html#timeseries-offset-aliases
        start_time (str, optional): 绘图开始的时间，指定时间格式为字符串并精确到秒，eg.'2020-01-01 01:00:00'，
                        默认为输入数据的第一个时间，不建议使用默认设置，建议设置初始时间为整点. Defaults to False.
        font (str, optional): 设置xlabel、title、text等字体设置，默认为Times New Roman、黑色、大小14, 
                        https://blog.csdn.net/Gou_Hailong/article/details/123628468. Defaults to None.
    """

    
    from MeteoPy import group_time

    # # 设置字体格式
    if not font:
        font = {'family': 'Times New Roman',
                'style': 'normal',  # 修改倾斜程度
                'weight': 'normal',  # 修改粗细
                'color': 'black',  # 颜色
                'size': 14,  # 字体大小
                }  # 设置xlabel、title、text等字体设置

    draw_time, draw_data = group_time(data, time, time_step, start_time, 2)
    # 绘图
    ax.grid(ls='--', lw=1, c='grey', alpha=0.6)  # 显示网格
    ax.boxplot(draw_data, labels=draw_time, sym="r+", showmeans=True)  # 绘制箱线图
    labels = [str(draw_time[i - 1])[:10] for i in ticks]  # 准备与上面指定的坐标轴的刻度对应替换的标签列表
    ax.set_yticks(ticks)
    ax.set_yticklabels(labels, fontdict=font, rotation=15)  # 倾斜15°


# # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # WRF/WPS # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # #

class WPS_domain():
    """根据namelist绘制WPS中的domain图

    >>> # 创建实例case1
    >>> WPS_domain('./namelist.wps')
    >>> plt.savefig('./WPS_domain.jpg', bbox_inches='tight', pad_inches=0.1, dpi=300)
    """

    def __init__(self, namelist_path : str, 
                 figsize : tuple = (5, 8), 
                 xticks : list = None, 
                 yticks : list = None, 
                 save_path : str = None):
        """创建实例时,获取初始参数

        Args:
            namelist_path (str): namelist地址
            figsize (tuple, optional): 设置画布fig的大小. Defaults to (5, 8).
            xticks (list, optional): 经度设置. Defaults to None.
            yticks (list, optional): 纬度设置. Defaults to None.
            save_path (list, optional): 图片保存地址. Defaults to None.
        """

        # 创建实例时,获取namelist.wps地址和读取位置参数
        self.namelist_path = namelist_path
        # 获取画布大小
        self.figsize = figsize
        self.xticks = xticks
        self.yticks = yticks
        self.save_path = save_path

        # 创建空字典，存放位置变量
        self.namelist = {}
        # 读取位置参数
        self.read_namelist()

        # # 调用方法
        self.d01()
        self.d02_()


    def read_namelist(self):
        """
            读取namelist.wps中的位置参数
        """

        import f90nml


        # # 读取namelist文件
        self.namelist_wps = f90nml.read(self.namelist_path)

        # 获取嵌套层数
        self.namelist['max_dom'] = self.namelist_wps['share']['max_dom']
        # 获取最外层嵌套的网格据
        self.namelist['dx'] = self.namelist_wps['geogrid']['dx']
        self.namelist['dy'] = self.namelist_wps['geogrid']['dy']
        # 获取网格数和起始格点
        self.namelist['e_we'] = self.namelist_wps['geogrid']['e_we']
        self.namelist['e_sn'] = self.namelist_wps['geogrid']['e_sn']
        self.namelist['i_parent_start'] = self.namelist_wps['geogrid']['i_parent_start']
        self.namelist['j_parent_start'] = self.namelist_wps['geogrid']['j_parent_start']
        # 获取嵌套网格放缩比例
        self.namelist['parent_grid_ratio'] = self.namelist_wps['geogrid']['parent_grid_ratio']
        # 获取最外层网格中心经纬度
        self.namelist['ref_lat'] = self.namelist_wps['geogrid']['ref_lat']
        self.namelist['ref_lon'] = self.namelist_wps['geogrid']['ref_lon']
        # 获取投影类型
        self.namelist['map_proj'] = self.namelist_wps['geogrid']['map_proj']
        self.namelist['truelat1'] = self.namelist_wps['geogrid']['truelat1']
        self.namelist['truelat2'] = self.namelist_wps['geogrid']['truelat2']


    def d01(self):
        """
            绘制d01
        """

        import cartopy.crs as ccrs
        import matplotlib.pyplot as plt


        # 计算网格边界与中线的偏移距离
        false_easting = (self.namelist['e_we'][0] - 1) / 2 * self.namelist['dx']
        false_northing = (self.namelist['e_sn'][0] - 1) / 2 * self.namelist['dy']

        # 设置兰伯特正形投影
        self.proj_lambert = ccrs.LambertConformal(
            central_longitude=self.namelist['ref_lon'],
            central_latitude=self.namelist['ref_lat'],
            standard_parallels=(self.namelist['truelat1'], self.namelist['truelat2']),
            cutoff=-30,
            false_easting=false_easting,
            false_northing=false_northing,
        )

        # # 创建空白画布，和兰伯特投影绘图对象
        self.fig = plt.figure(figsize=self.figsize)
        self.ax = self.fig.add_subplot(1, 1, 1, projection=self.proj_lambert)
        # # 根据实际距离截取区域范围
        self.ax.set_extent([0, false_easting * 2, 0, false_northing * 2], crs=self.proj_lambert)

        # # 设置地图底图
        draw = Draw_map()
        draw.comunity_maps(self.ax, basemape=['海岸线'], cnmap={'level':'省'}, 
                           xticks=self.xticks, yticks=self.yticks)

        # # 标注d01, 这个位置需要根据经纬度手动调整
        self.ax.text(0.92, 0.955, 'd01', transform=self.ax.transAxes, fontdict={'size': 10, 'weight':'bold'})

    def d02_(self):
        """
            在d01中圈出其他嵌套范围
        """

        import numpy as np

        # # 循环圈制
        ll_lon, ll_lat = 0, 0  # 左下角设为0
        ratio1, ratio2 = 1, 1
        for i in range(2, self.namelist['max_dom'] + 1):
            ratio2 *= self.namelist['parent_grid_ratio'][i - 1]
            # 计算四个点在d01的相对距离
            ll_lon += self.namelist['dx'] / ratio1 * (self.namelist['i_parent_start'][i - 1] - 1)
            ll_lat += self.namelist['dy'] / ratio1 * (self.namelist['j_parent_start'][i - 1] - 1)
            ur_lon = ll_lon + self.namelist['dx'] / ratio2 * (self.namelist['e_we'][i - 1] - 1)
            ur_lat = ll_lat + self.namelist['dy'] / ratio2 * (self.namelist['e_sn'][i - 1] - 1)

            lon = np.empty(4)
            lat = np.empty(4)

            lon[0], lat[0] = ll_lon, ll_lat  # lower left (ll)
            lon[1], lat[1] = ur_lon, ll_lat  # lower right (lr)
            lon[2], lat[2] = ur_lon, ur_lat  # upper right (ur)
            lon[3], lat[3] = ll_lon, ur_lat  # upper left (ul)

            ratio1 *= self.namelist['parent_grid_ratio'][i - 1]

            # 画图
            self.ax.plot([lon[0], lon[1]], [lat[0], lat[1]], color='black', linewidth=1.2,
                         transform=self.proj_lambert)
            self.ax.plot([lon[1], lon[2]], [lat[1], lat[2]], color='black', linewidth=1.2,
                         transform=self.proj_lambert)
            self.ax.plot([lon[2], lon[3]], [lat[2], lat[3]], color='black', linewidth=1.2,
                         transform=self.proj_lambert)
            self.ax.plot([lon[3], lon[0]], [lat[3], lat[0]], color='black', linewidth=1.2,
                         transform=self.proj_lambert)

            self.ax.text(lon[2] - 25 * self.namelist['dx'] / ratio2,
                         lat[2] - 15 * self.namelist['dy'] / ratio2,
                         'd0' + str(i), transform=self.proj_lambert, fontdict={'size': 10, 'weight':'bold'})
            
        # save_path
        if self.save_path:
            self.fig.savefig(self.save_path, bbox_inches='tight', pad_inches=0.1, dpi=300)


class Landuse_geo():
    """在WPS中使用绘制土地利用类型图

    >>> # 创建实例case1
    >>> case1 = Landuse_geo('./namelist.wps')
    >>> case1.d01_hgt('geo_em.d01.nc')
    >>> case1.Landuse('geo_em.d02.nc')
    >>> plt.savefig('./Landuse_geo.jpg', bbox_inches='tight', pad_inches=0.1, dpi=300)
    """

    def __init__(self, namelist_path : str, 
                 save_path : str = None):
        
        # 创建实例时,获取namelist.wps地址
        self.namelist_path = namelist_path
        self.save_path = save_path

        # 创建空字典，存放位置变量
        self.namelist = {}
        # 读取位置参数
        self.read_namelist()

    def read_namelist(self):
        """
            读取namelist.wps中的位置参数
        """

        import f90nml

        # # 读取namelist文件
        self.namelist_wps = f90nml.read(self.namelist_path)

        # 获取嵌套层数
        self.namelist['max_dom'] = self.namelist_wps['share']['max_dom']
        # 获取最外层嵌套的网格据
        self.namelist['dx'] = self.namelist_wps['geogrid']['dx']
        self.namelist['dy'] = self.namelist_wps['geogrid']['dy']
        # 获取网格数和起始格点
        self.namelist['e_we'] = self.namelist_wps['geogrid']['e_we']
        self.namelist['e_sn'] = self.namelist_wps['geogrid']['e_sn']
        self.namelist['i_parent_start'] = self.namelist_wps['geogrid']['i_parent_start']
        self.namelist['j_parent_start'] = self.namelist_wps['geogrid']['j_parent_start']
        # 获取嵌套网格放缩比例
        self.namelist['parent_grid_ratio'] = self.namelist_wps['geogrid']['parent_grid_ratio']
        # 获取最外层网格中心经纬度
        self.namelist['ref_lat'] = self.namelist_wps['geogrid']['ref_lat']
        self.namelist['ref_lon'] = self.namelist_wps['geogrid']['ref_lon']
        # 获取投影类型
        self.namelist['map_proj'] = self.namelist_wps['geogrid']['map_proj']
        self.namelist['truelat1'] = self.namelist_wps['geogrid']['truelat1']
        self.namelist['truelat2'] = self.namelist_wps['geogrid']['truelat2']


    def d01_hgt(self, geo_d01 : str):
        """
            d01绘制地形HGT
        """

        import cmaps
        import numpy as np
        import cartopy.crs as ccrs
        from netCDF4 import Dataset
        import matplotlib.pyplot as plt
        import cartopy.feature as cfeature
        from cnmaps import get_adm_maps, draw_maps, clip_contours_by_map
        from wrf import to_np, getvar, get_cartopy, cartopy_xlim, cartopy_ylim, latlon_coords


        # # 分别读取d01的下垫面数据
        ncfile_d01 = Dataset(geo_d01)
        # # 分别提取d01对应的位置高度
        hgt_d01 = getvar(ncfile_d01, 'HGT_M')
        # # 获取经纬度信息
        lats_d01, lons_d01 = latlon_coords(hgt_d01)
        # 获取地图投影信息
        cart_proj = get_cartopy(hgt_d01)

        # # 创建第一个绘图对象d01
        self.fig = plt.figure(figsize=(5, 10))
        self.ax = self.fig.add_subplot(2, 1, 1, projection=cart_proj)
        # 设置范围
        self.ax.set_xlim(cartopy_xlim(hgt_d01))
        self.ax.set_ylim(cartopy_ylim(hgt_d01))

        # # 高度填色
        con = self.ax.contourf(to_np(lons_d01), to_np(lats_d01), to_np(hgt_d01), levels=np.arange(0, 1900, 200),
                               extend='both', cmap=cmaps.MPL_terrain, transform=ccrs.PlateCarree())
        # # 设置网格
        gl = self.ax.gridlines(xlocs=np.arange(115, 124.1, 2), ylocs=np.arange(28, 38.1, 2),
                               x_inline=False, y_inline=False, draw_labels=True, linestyle="dotted",
                               linewidth=1, alpha=0.4)
        gl.top_labels = False  # 关闭上方刻度
        gl.right_labels = False  # 关闭右侧刻度
        gl.rotate_labels = False  # 关闭刻度旋转

        # 添加色标
        position = self.fig.add_axes([0.85, 0.55, 0.018, 0.32])  # 坐标＋长宽
        cbar = self.fig.colorbar(con, shrink=1, cax=position, orientation='vertical')
        cbar.set_label('m')
        cbar.set_ticks(np.arange(0, 1900, 200))
        # cbar.ax.set_yticklabels(labels)

        # # 添加省界
        # map_polygon = get_adm_maps(country='中华人民共和国', record='first', only_polygon=True)
        # clip_contours_by_map(con, map_polygon, self.ax)  # 根据地图剪切填色图
        draw_maps(get_adm_maps(level='省'), self.ax, linewidth=0.5, color='k')

        # # 添加背景
        # self.ax.stock_img()
        # self.ax.add_feature(cfeature.LAND)  # 添加陆地
        # self.ax.add_feature(cfeature.RIVERS, lw=0.3)  # 添加河流
        self.ax.add_feature(cfeature.COASTLINE, lw=0.3)
        # self.ax.add_feature(cfeature.LAKES) # 添加湖泊
        # self.ax.add_feature(cfeature.OCEAN) # 添加海洋

        # # d01标签
        self.ax.text(0.89, 0.955, 'd01', fontsize=10, fontweight='bold', transform=self.ax.transAxes)

        # # 绘制d02_3_4
        for i in range(2, self.namelist['max_dom'] + 1):
            # 读取d0_下垫面数据
            ncfile_d0_ = Dataset(geo_d01[:-4] + str(i) + '.nc')
            hgt_d0_ = getvar(ncfile_d0_, 'HGT_M')
            lats_d0_, lons_d0_ = latlon_coords(hgt_d0_)
            self.ax.plot([lons_d0_[0, 0], lons_d0_[-1, 0]], [lats_d0_[0, 0], lats_d0_[-1, 0]],
                         color='k', lw=1., transform=ccrs.PlateCarree())
            self.ax.plot([lons_d0_[-1, 0], lons_d0_[-1, -1]], [lats_d0_[-1, 0], lats_d0_[-1, -1]],
                         color='k', lw=1., transform=ccrs.PlateCarree())
            self.ax.plot([lons_d0_[-1, -1], lons_d0_[0, -1]], [lats_d0_[-1, -1], lats_d0_[0, -1]],
                         color='k', lw=1., transform=ccrs.PlateCarree())
            self.ax.plot([lons_d0_[0, -1], lons_d0_[0, 0]], [lats_d0_[0, -1], lats_d0_[0, 0]],
                         color='k', lw=1., transform=ccrs.PlateCarree())

            # # d0m标签
            # self.ax.text(0.995, 0.945, 'd01', fontsize=10, fontweight='bold', transform=self.ax.transAxes)

    def Landuse(self, geo_d0m : str):
        """
            最内层土地利用
        """

        import numpy as np
        import cartopy.crs as ccrs
        from netCDF4 import Dataset
        from MeteoPy import LU_MODIS21, mark_inset
        from wrf import to_np, getvar, get_cartopy, cartopy_xlim, cartopy_ylim, latlon_coords


        # 读取nc数据,获取最内层嵌套土地利用
        ncfile = Dataset(geo_d0m)
        landuse = getvar(ncfile, 'LU_INDEX')

        # 获取经纬度信息
        lats, lons = latlon_coords(landuse)
        # 获取地图投影信息
        cart_proj = get_cartopy(landuse)

        # # 创建空白画布
        self.ax1 = self.fig.add_subplot(2, 1, 2, projection=cart_proj)
        # 设置范围
        self.ax1.set_xlim(cartopy_xlim(landuse))
        self.ax1.set_ylim(cartopy_ylim(landuse))

        # 调用颜色和标签
        cm, labels = LU_MODIS21()
        im = self.ax1.pcolormesh(to_np(lons), to_np(lats), to_np(landuse), vmin=1,
                                 vmax=len(labels) + 1, cmap=cm, transform=ccrs.PlateCarree())
        gl = self.ax1.gridlines(x_inline=False, y_inline=False, draw_labels=True,
                                linestyle="--", linewidth=1, alpha=0.5)
        gl.top_labels = False  # 关闭上方刻度
        gl.right_labels = False  # 关闭右侧刻度
        gl.rotate_labels = False  # 关闭刻度旋转

        # 添加色标
        position = self.fig.add_axes([0.90, 0.13, 0.018, 0.31])  # 坐标＋长宽
        cbar = self.fig.colorbar(im, shrink=1, cax=position, orientation='vertical')
        cbar.set_ticks(np.arange(1.5, len(labels) + 1))
        cbar.ax.set_yticklabels(labels)

        # 子图连接
        mark_inset(self.ax, self.ax1, loc1a=2, loc1b=3, loc2a=1, loc2b=4, fc='none', ec='black', lw=1.2)

        # # d0m标签
        self.ax1.text(0.9, 0.955, 'd0' + geo_d0m[-4], fontsize=10, fontweight='bold', transform=self.ax1.transAxes)

        # save_path
        if self.save_path:
            self.fig.savefig(self.save_path, bbox_inches='tight', pad_inches=0.1, dpi=300)

















