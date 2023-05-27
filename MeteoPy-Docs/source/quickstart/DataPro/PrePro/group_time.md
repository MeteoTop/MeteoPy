# group_time()
```python
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
```

