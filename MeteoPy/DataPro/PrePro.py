# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author      :   nhno 
# @Time        :   2023/04/04 20:45:51
# @Description :   本脚本中主要存放一些数据前处理的函数
#                  1. heavy_sampling_method(): 重抽样函数（固定时间间隔的平均值）,功能：对输入的以时间为索引的DataFrame数组中的所有列数据进行重抽样处理;
#                  2. group_time(): 根据时间间隔step进行分组，eg.可用于绘制箱线图的数据预处理;
#                  3. Nan_3sigma(): 利用3σ原则剔除数据野点，将原始数据标准化处理之后，将标准化后绝对值大于3的即为nan;


def heavy_sampling_method(data, 
                          start_time : str, 
                          end_time : str, 
                          step : str, 
                          function : str, 
                          type : int = 0):
    
    """重抽样函数（固定时间间隔的平均值）
       功能：对输入的以时间为索引的DataFrame数组中的所有列数据进行重抽样处理

    Args:
        data (DataFrame): 输入待处理数据，其必须为DataFrame数组格式，索引为datetime格式的时间(年-月-日 时:分:秒);
        start_time (str): 重抽样开始时间，格式为'年-月-日 时:分:秒';
        end_time (str): 重抽样结束时间，格式为'年-月-日 时:分:秒';
        step (str): 重抽样步长，需为字符串格式，eg."1Y/y","1M/m",“10D/d”,"30min","1H/h","30S/s";:M/m表示月，min表示分钟;
        function (str): 对分组数据进行一些计算，目前仅支持平均值()'mean')or求和()'sum');
        type (int, optional): 设置重抽样格式,
                              0为向后重抽样左开右闭00：30的值为(00:00,00:30],
                              1为向后重抽样左闭右开00：30的值为[00:00,00:30),
                              2为向前重抽样左开右闭00：30的值为(00:30,01:00],
                              3为向前重抽样左闭右开00：30的值为[00:30,01:00). Defaults to 0.

    Returns:
        DataFrame: 返回重抽样的结果,为DataFrame格式数组
    """
    
    
    import time
    import pandas as pd
    from datetime import datetime, timedelta
    from dateutil.relativedelta import relativedelta

    # 计算程序开始时间
    time_begin = time.time()

    # 生成重抽样时间标签，起止时间-按分钟生成时间
    start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')  # 将开始时间转化为datetime格式
    end_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')  # 将结束时间转化为datetime格式
    if step[-1] == 'M' or step[-1] == 'm':  # if the step is month
        heavy_sampling_time = pd.date_range(start_time, end_time, freq=step[:-1] + 'MS')  # start month frequency
    else:
        heavy_sampling_time = pd.date_range(start_time, end_time, freq=step)
    print(heavy_sampling_time)

    # 将如果字符串step为月以下尺度，则将setp转换成以秒为单位
    # 将如果字符串step为月及以上尺度，则将setp转换成以月为单位
    if step[-1] == 'S' or step[-1] == 's':  # second
        step_ = float(step[:-1])
    elif step[-1] == 'n':  # minute
        step_ = float(step[:-3]) * 60
    elif step[-1] == 'H' or step[-1] == 'h':  # hour
        step_ = float(step[:-1]) * 60 * 60
    elif step[-1] == 'D' or step[-1] == 'd':  # day
        step_ = float(step[:-1]) * 24 * 60 * 60
    elif step[-1] == 'M' or step[-1] == 'm':  # month
        step_ = float(step[:-1])
    elif step[-1] == 'Y' or step[-1] == 'y':  # year
        step_ = float(step[:-1]) * 12
    else:
        print('The entering step is error!')

    # # 计算重抽样结果
    heavy_sampling = pd.DataFrame([], columns=data.columns)  # 创建空DataFrame数组，方便后面添加
    if type == 0:
        # 计算第一个时间点的重抽样值
        for i in range(len(heavy_sampling_time)):  # 按heavy_sampling_time循环，计算每个时间点的重抽样值
            if i == 0:  # 对于第一个时间，需要特殊处理，获得该时次与其前step时间之间的数据
                if step[-1] in ['S', 'n', 'H', 'D', 's', 'h', 'd']:
                    start = heavy_sampling_time[i] + timedelta(seconds=-1 * step_)
                elif step[-1] in ['M', 'Y', 'm', 'y']:
                    start = heavy_sampling_time[i] + relativedelta(months=-1 * step_)
            else:
                start = heavy_sampling_time[i - 1]
            end = heavy_sampling_time[i]
            heavy_range = data.loc[start:end]
            if len(heavy_range) > 0 and heavy_range.index[0] == start:
                heavy_range = heavy_range.drop(heavy_range.index[0], axis=0)  # 若heavy_range第一个时间为start，则删除
            if len(heavy_range) > 0:
                if function == 'mean':
                    temp = heavy_range.mean(axis=0)  # 计算平均值
                elif function == 'sum':
                    temp = heavy_range.sum(axis=0)  # 计算和
                heavy_sampling.loc[heavy_sampling_time[i]] = temp
                # # 重抽样计时
                time_new = time.time()
                print('重抽样计算:' + str(heavy_sampling_time[i])[:19] + '  用时:' + str(time_new - time_begin) + 's')

    if type == 1:
        # 计算第一个时间点的重抽样值
        for i in range(len(heavy_sampling_time)):  # 按heavy_sampling_time循环，计算每个时间点的重抽样值
            if i == 0:  # 对于第一个时间，需要特殊处理，获得该时次与其前step时间之间的数据
                if step[-1] in ['S', 'n', 'H', 'D', 's', 'h', 'd']:
                    start = heavy_sampling_time[i] + timedelta(seconds=-1 * step_)
                elif step[-1] in ['M', 'Y', 'm', 'y']:
                    start = heavy_sampling_time[i] + relativedelta(months=-1 * step_)
            else:
                start = heavy_sampling_time[i - 1]
            end = heavy_sampling_time[i]
            heavy_range = data.loc[start:end]
            if len(heavy_range) > 0 and heavy_range.index[-1] == end:
                heavy_range = heavy_range.drop(heavy_range.index[-1], axis=0)  # 若heavy_range第一个时间为start，则删除
            if len(heavy_range) > 0:
                if function == 'mean':
                    temp = heavy_range.mean(axis=0)  # 计算平均值
                elif function == 'sum':
                    temp = heavy_range.sum(axis=0)  # 计算和
                heavy_sampling.loc[heavy_sampling_time[i]] = temp
                # # 重抽样计时
                time_new = time.time()
                print('重抽样计算:' + str(heavy_sampling_time[i])[:19] + '  用时:' + str(time_new - time_begin) + 's')

    if type == 2:
        for i in range(len(heavy_sampling_time)):  # 按heavy_sampling_time循环，计算每个时间点的重抽样值
            start = heavy_sampling_time[i]
            if i == len(heavy_sampling_time) - 1:  # 对于第一个时间，需要特殊处理，获得该时次与其前step时间之间的数据
                if step[-1] in ['S', 'n', 'H', 'D', 's', 'h', 'd']:
                    end = heavy_sampling_time[i] + timedelta(seconds=step_)
                elif step[-1] in ['M', 'Y', 'm', 'y']:
                    end = heavy_sampling_time[i] + relativedelta(months=step_)
            else:
                end = heavy_sampling_time[i + 1]
            heavy_range = data.loc[start:end]
            if len(heavy_range) > 0 and heavy_range.index[0] == start:
                heavy_range = heavy_range.drop(heavy_range.index[0], axis=0)  # 若heavy_range最后时间为end，则删除
            if len(heavy_range) > 0:
                if function == 'mean':
                    temp = heavy_range.mean(axis=0)  # 计算平均值
                elif function == 'sum':
                    temp = heavy_range.sum(axis=0)  # 计算和
                heavy_sampling.loc[heavy_sampling_time[i]] = temp
                # # 重抽样计时
                time_new = time.time()
                print('重抽样计算:' + str(heavy_sampling_time[i])[:19] + '  用时:' + str(time_new - time_begin) + 's')

    if type == 3:
        for i in range(len(heavy_sampling_time)):  # 按heavy_sampling_time循环，计算每个时间点的重抽样值
            start = heavy_sampling_time[i]
            if i == len(heavy_sampling_time) - 1:  # 对于第一个时间，需要特殊处理，获得该时次与其前step时间之间的数据
                if step[-1] in ['S', 'n', 'H', 'D', 's', 'h', 'd']:
                    end = heavy_sampling_time[i] + timedelta(seconds=step_)
                elif step[-1] in ['M', 'Y', 'm', 'y']:
                    end = heavy_sampling_time[i] + relativedelta(months=step_)
            else:
                end = heavy_sampling_time[i + 1]
            heavy_range = data.loc[start:end]
            if len(heavy_range) > 0 and heavy_range.index[-1] == end:
                heavy_range = heavy_range.drop(heavy_range.index[-1], axis=0)  # 若heavy_range最后时间为end，则删除
            if len(heavy_range) > 0:
                if function == 'mean':
                    temp = heavy_range.mean(axis=0)  # 计算平均值
                elif function == 'sum':
                    temp = heavy_range.sum(axis=0)  # 计算和
                heavy_sampling.loc[heavy_sampling_time[i]] = temp
                # # 重抽样计时
                time_new = time.time()
                print('重抽样计算:' + str(heavy_sampling_time[i])[:19] + '  用时:' + str(time_new - time_begin) + 's')
    
    return heavy_sampling


def group_time(data : list, 
               time : list, 
               group_time_step : str, 
               group_start_time : str = None, 
               lim_long : int = 1):
    
    """根据时间间隔group_time_step进行分组，eg.可用于绘制箱线图的数据预处理

    Args:
        data (list): 欲分组数据，建议使用list或者numpy格式，一维数组;
        time (list): 欲分组数据对应时间，建议使用list或者numpy格式，且时间本身需转化时间格式datatime;
        group_time_step (str): 指定分组时间间隔，参照https://pandas.pydata.org/docs/user_guide/timeseries.html#timeseries-offset-aliases;
        group_start_time (str, optional): 对时间分组，开始的时间，指定时间格式为字符串并精确到秒，eg.'2020-01-01 01:00:00'，
                                 默认为输入数据的第一个时间，不建议使用默认设置，建议设置初始时间为整点;. Defaults to None.
        lim_long (int, optional): 每组数据长度的下限，默认为1，即每组至少有一个数据，没有数据的组将被删除. Defaults to 1.

    Returns:
        _type_: _description_
    """

    import copy
    import pandas as pd
    from datetime import datetime


    # # 将分组数据与时间对应起来
    data = pd.Series(data, index=time)
    # # 根据时间间隔生成时间列表
    if group_start_time:
        start_time = datetime.strptime(group_start_time, '%Y-%m-%d %H:%M:%S')
        group_time = pd.date_range(start_time, data.index[-1], freq=group_time_step)  # 生成绘图时间
        # 补全首末时间
        if group_time[0] != start_time:
            group_time = group_time.insert(0, start_time)
        if group_time[-1] != data.index[-1]:
            group_time = group_time.insert(len(group_time), data.index[-1])
    else:
        group_time = pd.date_range(data.index[0], data.index[-1], freq=group_time_step)  # 生成分组时间
        # 补全首末时间
        if group_time[0] != data.index[0]:
            group_time = group_time.insert(0, data.index[0])
        if group_time[-1] != data.index[-1]:
            group_time = group_time.insert(len(group_time), data.index[-1])
        
    #     print(group_time_box)
    group_data = []  # 储存绘图数据
    temp_group_time = copy.deepcopy(group_time)  # 复制时间，方便后面处理
    for i in range(len(temp_group_time) - 1):
        temp = data.loc[temp_group_time[i]:temp_group_time[i + 1]]
        temp = temp.dropna(axis=0, how='all')  # 删除所有缺省数据NAN
        if len(temp) < lim_long:
            group_time = group_time.drop(temp_group_time[i])  # 删除没有数据的时段，只有数据大于2才能画箱线图
        else:
            if temp.index[-1] == temp_group_time[i + 1] and i != len(temp_group_time) - 2:
                temp = temp.drop(temp.index[-1], axis=0)
            group_data.append(list(temp.values))
    #     print(group_time)
    
    return group_time, group_data


def Nan_3sigma(data : list):

    """利用3σ原则剔除数据野点，将原始数据标准化处理之后，将标准化后绝对值大于3的即为nan

    Args:
        data (list): 欲处理数据，可以为list、numpy或dataframe格式，一/多维数组，本程序仅对列处理;

    Returns:
        numpy or DataFrame: 返回剔除野点之后的结果;
    """

    import numpy as np
    import copy


    data_copy = copy.deepcopy(data)
    # 标准化处理
    try:  # 处理pandas数组
        data_copy_standard = (data_copy - data_copy.mean(axis=0)) / data_copy.std(axis=0)
        # 剔除方差绝对值大于3.0的数据，记录为NAN
        for i in range(data_copy.shape[1]):
            data_copy.iloc[:, i].iloc[data_copy_standard.iloc[:, i].abs() >= 3.0] = np.nan
    except:  # 处理numpy数组
        data_copy = np.array(data_copy)
        # 将整型的numpy数组改为浮点型，不然后面替换nan的时候会报错
        data_copy = data_copy.astype(float)
        data_copy_standard = (data_copy - np.mean(data_copy, axis=0)) / np.std(data_copy, axis=0)
        # 剔除方差绝对值大于3.0的数据，记录为NAN
        for i in range(data_copy.shape[1]):
            data_copy[:, i][np.abs(data_copy_standard[:, i]) >= 3.0] = np.nan

    return data_copy


# # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # WRF/WPS # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # #

class WRF_Chem_getvars():
    """由于WRF-chem输出的结果没有'经纬度'及'时间'信息，并且对于长时间模拟，
    通常会输出多个文件，不利于随后的数据处理。本程序主要实现如下功能：
    1. 重铸输出数据的维度信息，本程序主要完成经纬度和时间维度的重铸：
        1.1 经纬度：依赖于wrf-python.xy_to_ll_proj函数，根据模式的中心经纬度、格距等信息，
                    计算各个格点对应的经纬度信息，最终结果类似于wrfout的经纬度；
        1.2 时间：依赖于各文件名，文件命名需以“年月日.nc”结尾(20230406.nc)。并且将时间修改为北京时间；
    2. 提取需要的变量信息，臭氧、PM2.5等，并将多个文件按时间维合并为1个nc;

    >>> # # 创建实例
    >>> path = './'
    >>> which = 'O3'
    >>> ncfile = './202007O3.nc'
    >>> case = WRF_Chem_getvars(path, which, ncfile)
    """

    def __init__(self, path : str, 
                 which : list, 
                 ncfile : str) -> None:
        """初始化变量

        Args:
            path (str): 存放WRF-Chem输出出数据的文件夹，文件名应有明显的时间顺序
            which (list): 哪一种污染物/哪几种污染物，eg，臭氧、PM2.5等
            ncfile (str): 最终合并的nc文件地址
        """

        self.path = path
        self.which = which  # 指定的污染物
        self.ncfile = ncfile  # 最终合并的nc文件地址

        # # 调用方法
        self.get_files()
        self.concat_nc()     


    def get_files(self):

        import os

        # 获取数据文件列表
        self.file_list = os.listdir(self.path)  # 获取数据文件夹中所以文件名
        self.file_list = list(filter(lambda x: x[-3:] == '.nc', self.file_list))  # 判断file_list是否是.nc，并返回是.nc的数组
        self.file_list = list(filter(lambda x: 'gcc' in x, self.file_list))  # 判断file_list是否是日数据，并返回是臭氧的数组
        self.file_list.sort()  # 排序
        self.file_list = [self.path + '/' + i for i in self.file_list]  # 补全地址


    def getvars(self, data):
        """提取WRF-chem输出数据的变量

        Args:
            data (dataset):  使用xarray.open_dataset()读取的nc数据
        """

        import copy
        import numpy as np


        # # 提取所有变量
        self.all_vars = []
        temp = data.data_vars  # 获取所有变量
        [self.all_vars.append(i) for i in temp]  # 转存变量名
        self.all_vars.remove('TFLAG')    # 除去变量TFLAG

        # # 获取排放源类型
        self.contro_var = {}    # 按排放类型储存PM2_5变量名
        for var in self.all_vars:
            self.contro_var[var[-3:]] = []     # 获取排放类型

        # # 根据排放源类型，对which指定污染物归类
        self.which = np.array([self.which]).reshape(-1)  # 如果为多个指定污染物，将其转化为以为的数组
        # 指定污染物字典初始化
        self.all_which_var = {}
        for i in self.which:
            self.all_which_var[i] = copy.deepcopy(self.contro_var)  # 深度复杂，不传递'地址'

        # # 获取每种排放类型的变量名
        for var in self.all_vars:
            try:
                if var.split('_')[0][-1] in ['I', 'J', 'K']:
                    try:
                        self.all_which_var['PM2.5'][var.split('_')[1]].append(var)
                    except (KeyError):
                        pass
                else:
                    self.all_which_var[var.split('_')[0]][var.split('_')[1]].append(var)
            except (KeyError):
                pass
            

    def creat_lat_lon(self, data):
        """重铸经纬度信息

        Args:
            data (dataset): 使用xarray.open_dataset()读取的nc数据

        Returns:
            dataset: 重铸经纬度信息之后的dataset格式数据
        """

        import numpy as np
        from wrf import xy_to_ll_proj


        # # 重组源排放数据经纬度信息
        x, y = np.meshgrid(data.COL, data.ROW)
        # # 根据网格点，中心经纬度，网格距等信息计算网格点对应的经纬度信息
        lat_lon = xy_to_ll_proj(x, y, squeeze=False, map_proj=1, truelat1=data.attrs['P_ALP'], truelat2=data.attrs['P_BET'], 
                    stand_lon=data.attrs['P_GAM'], ref_lat=data.attrs['YCENT'], ref_lon=data.attrs['XCENT'], 
                    known_x=(data.attrs['NCOLS'] - 1) / 2 + 1, known_y=(data.attrs['NROWS'] - 1) / 2 + 1, 
                    dx=data.attrs['XCELL'], dy=data.attrs['YCELL'])

        lat = np.array(lat_lon.loc['lat']).reshape((data.attrs['NROWS'], data.attrs['NCOLS']))  # (纬度，经度))
        lon = np.array(lat_lon.loc['lon']).reshape((data.attrs['NROWS'], data.attrs['NCOLS']))
        # # 重组源排放数据经纬度信息
        data.coords['lon'] = (('ROW', 'COL'), lon)
        data.coords['lat'] = (('ROW', 'COL'), lat)

        return data
    

    def concat_nc(self):
        """
            添加经纬度信息、修改时间维度，并合并nc数据
        """

        import xarray as xr
        from datetime import datetime, timedelta


        # # 合并7月份的所有数据
        self.all_data = []
        for file in self.file_list:
            self.data = xr.open_dataset(file)
            # # 获取指定变量名
            self.getvars(self.data)

            # # 修改时间维度信息，转化为标准datatime时间格式
            time = datetime.strptime(file.split('\\')[-1][-11:-3], '%Y%m%d')
            t = [time + timedelta(hours=int(i) + 8) for i in self.data.TSTEP.values]
            self.data.coords['TSTEP'] = t
            # # 修改经纬度信息
            self.data = self.creat_lat_lon(self.data)
            
            # # 截取变量
            self.cut_var = {}
            for i in self.all_which_var:      # 循环污染物
                    for j in self.all_which_var[i]:     # 循环源
                        if i != 'PM2.5':
                            if len(self.all_which_var[i][j]) == 1:
                                for k in self.all_which_var[i][j]:
                                    self.cut_var[k] = self.data[k]
                            else:
                                print(i + '物理量同一源不止一个变量，请查看all_which_var')
                                break
                        else:
                            temp = 0
                            for k in self.all_which_var[i][j]:
                                temp = temp + self.data[k]
                            self.cut_var['PM2.5_' + j] = temp

            self.cut_var = xr.Dataset(self.cut_var)
            # 添加到all_data当中
            self.all_data.append(self.cut_var)
            print(file + ': 合并完成！')
        self.all_data = xr.concat(self.all_data, dim='TSTEP')
        self.all_data.to_netcdf(self.ncfile)
        print('合并完成！')















