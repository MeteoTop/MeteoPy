# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author      :   nhno 
# @Time        :   2023/05/23 13:58:53
# @Description :   统计函数


def RMSE(data1 : list, 
         data2 : list, 
         axis : int = 0):
    """计算均方根误差

    Args:
        data1 (list): 1/2维数组，至多2维
        data2 (list): 1/2维数组，至多2维
        axis (int, optional): 当数据为2维的时候，指定对哪一维计算RMSE. Defaults to 0.
                              axis=0是，列与列计算, axis=1时，data1与data2行与行计算

    Raises:
        Exception: _description_

    Returns:
        _type_: RMSE
    """


    import numpy as np

    # # 将数据转化为numpy格式
    data1 = np.array(data1)
    data2 = np.array(data2)

    if data1.shape != data2.shape:
        raise Exception("data1.shape=", data1.shape, ", data2.shape=", data2.shape,
                        ", data1和data2数据长度不同")
    else:
        if len(data1.shape) == 1:
            return np.sqrt(np.sum((data1 - data2) ** 2, axis=0) / data1.shape[0])
        elif len(data1.shape) == 2:
            return np.sqrt(np.sum((data1 - data2) ** 2, axis=axis) / data1.shape[axis])
        elif len(data1.shape) > 2:
            raise Exception("data1.shape=", data1.shape, ", data1只能为1/2维")


def MAE(data1 : list, 
        data2 : list, 
        axis : int = 0):
    """计算绝对误差

    Args:
        data1 (list): 1/2维数组，至多2维
        data2 (list): 1/2维数组，至多2维
        axis (int, optional): 当数据为2维的时候，指定对哪一维计算RMSE. Defaults to 0.
                              axis=0是，列与列计算, axis=1时，data1与data2行与行计算

    Raises:
        Exception: _description_

    Returns:
        _type_: MAE
    """


    import numpy as np

    # # 将数据转化为numpy格式
    data1 = np.array(data1)
    data2 = np.array(data2)

    if data1.shape != data2.shape:
        raise Exception("data1.shape=", data1.shape, ", data2.shape=", data2.shape,
                        ", data1和data2数据长度不同")
    else:
        if len(data1.shape) == 1:
            return np.sum(np.absolute(data1 - data2), axis=0) / data1.shape[0]
        elif len(data1.shape) == 2:
            return np.sum(np.absolute(data1 - data2), axis=axis) / data1.shape[axis]
        elif len(data1.shape) > 2:
            raise Exception("data1.shape=", data1.shape, ", data1只能为1/2维")


def contrast(data1 : list, 
             data2 : list, 
             axis : int = 0):
    """data1和data2的差异分析，RSME，MAE，R

    Args:
        data1 (list): 1/2维数组，至多2维
        data2 (list): 1/2维数组，至多2维
        axis (int, optional): 当数据为2维的时候，指定对哪一维计算RMSE. Defaults to 0.
                              axis=0是，列与列计算, axis=1时，data1与data2行与行计算
    """
    
    # https://blog.csdn.net/weixin_42414714/article/details/109023125
    # pearsonr计算的p值表示拒绝H0（x与y相关）的概率，与alpha相对应


    import numpy as np
    import pandas as pd
    from scipy.stats import pearsonr

    # # 将数据转化为numpy格式
    data1 = np.array(data1)
    data2 = np.array(data2)

    if data1.shape != data2.shape:
        raise Exception("data1.shape=", data1.shape, ", data2.shape=", data2.shape,
                        ", data1和data2数据长度不同")
    else:
        if len(data1.shape) == 1:
            result = pd.DataFrame([], index=[0], columns=['MAE', 'RMSE', 'R', 'P-value'])
            
            result['MAE'] = MAE(data1, data2)
            result['RMSE'] = RMSE(data1, data2)
            result['R'], result['P-value'] = pearsonr(data1, data2)
        elif len(data1.shape) == 2:
            result = pd.DataFrame([], index=np.arange(data1.shape[np.abs(axis - 1)]), 
                                columns=['MAE', 'RMSE', 'R', 'P-value'])
            
            result['MAE'] = MAE(data1, data2, axis=axis)
            result['RMSE'] = RMSE(data1, data2, axis=axis)
            for i in np.arange(data1.shape[np.abs(axis - 1)]):
                if axis == 0:
                    result.iloc[i, 2], result.iloc[i, 3] = pearsonr(data1[:, i], data2[:, i])
                elif axis == 1:
                    result.iloc[i, 2], result.iloc[i, 3] = pearsonr(data1[i, :], data2[i, :])
        elif len(data1.shape) > 2:
            raise Exception("data1.shape=", data1.shape, ", data1只能为1/2维")

    return result