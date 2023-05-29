# heavy_sampling_method()
heavy_sampling_method(data, 
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