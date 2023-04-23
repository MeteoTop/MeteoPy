# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author      :   nhno 
# @Time        :   2023/04/22 12:45:48
# @Description :   此脚本存放一些在定义函数时，变量初始化的工具函数
#                  1. dict_default(): 对于字典类的形参进行初始化，使调用父函数时字典形参可以省略部分键-值


def dict_default(var : dict, 
                 default : dict) -> dict:
    """对于字典类的形参进行初始化，使调用父函数时字典形参可以省略部分键-值

    Args:
        var (dict): 父函数中的字典形参
        default (dict): 字典形参默认值

    Raises:
        Exception: 如果var中的键不在默认值中，则引出异常Exception。
                   注意：这里不用KeyError，因为在try except语句中用到了KeyError。

    Returns:
        dict: 返回初始化后的var
    """
   

    # # 判断用户输入的字典var中的健是否‘合法’(是否在default中)
    for key in var.keys():
        if key not in default.keys():
            raise Exception("Invalid key: " + key)

    for key in default.keys():
        try:
            var[key]
        except KeyError:
            var[key] = default[key]
    
    return var