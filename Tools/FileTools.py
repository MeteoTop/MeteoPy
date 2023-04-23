# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author      :   nhno 
# @Time        :   2023/04/16 11:10:35
# @Description :   此文件下存放一些文本/文件夹处理的小工具
#                  1. vlookup(): 对DataFrame类型数据进行查找筛选;
#                  2. del_suffix(): 删除指定文件夹下，指定后缀名的文件（无论嵌套层数）;
#                  3. pdf_concat(): 合并指定文件夹下的所有pdf文件;
#                  4. get_Innermost_file(): 获取文件夹最内层的数据文件，主要用于多层文件嵌套时;


def vlookup(Filtered_column : str, 
            To_filter_column : str, 
            file_Filtered : str = None, 
            Filtered : list = None, 
            file_To_filter : str = None, 
            To_filter : list = None):
    
    """依据file_To_filter文件中的To_filter_column列，
       与file_Filtered文件Filtered_column列相匹配，提取Filtered文件中的相应行，


    Args:
        Filtered_column (str): 被筛选的列名;
        To_filter_column (str): 拟筛选的列名;
        file_Filtered (str, optional): 被筛选excel的文件地址，仅支持excel和csv. Defaults to None.
        Filtered (list, optional): 被筛选的DataFrame格式的数组. Defaults to None.
        file_To_filter (str, optional): 拟筛选excel的文件地址，仅支持excel和csv. Defaults to None.
        To_filter (list, optional): 拟筛选DataFrame格式的数组. Defaults to None.

    Returns:
        DataFrame: 返回一个筛选好后的DataFrame数组
    """

    import pandas as pd


    # 读取数据
    if Filtered is None and To_filter is None:  # 判断是否传入文件地址
        if file_Filtered[-5:] == '.xlsx' and file_To_filter[-5:] == '.xlsx':
            Filtered = pd.read_excel(file_Filtered)
            To_filter = pd.read_excel(file_To_filter)
        elif file_Filtered[-4:] == '.csv' and file_To_filter[-4:] == '.csv':
            Filtered = pd.read_csv(file_Filtered)
            To_filter = pd.read_csv(file_To_filter)

    df = pd.DataFrame([], columns=Filtered.columns)  # 创建空DataFrame数组，存放从Filtered中选出来的数据
    for i in To_filter[To_filter_column]:
        temp = Filtered.loc[Filtered[Filtered_column] == i]  # 从Filtered中提取与To_filter中第一个相对应的行
        df = pd.concat([df, temp], axis=0)  # 将筛选出来的行合并
    # 更改df索引为0-n
    df.reset_index(drop=True, inplace=True)

    return df


def del_suffix(path : str, 
               del_file_suffix : str):
    """删除指定文件夹下的所有指定后缀的文件，包括嵌套文件中的指定后缀的文件

    Args:
        path (str): 指定文件夹
        del_file_suffix (str): 欲删除文件后缀名
    """

    import os


    for cur_file in os.scandir(path):
        f_name = path + '\\' + str(cur_file.name)  # 补全文件路径
        if cur_file.is_file() and cur_file.name[-1 * len(del_file_suffix):] == del_file_suffix:  # 删除文件后缀为.del_suffix的文件
            os.remove(f_name)
        if cur_file.is_dir():  # 递归调用del_suffix函数
            del_suffix(f_name, del_file_suffix)


def pdf_concat(path : str, 
               result_file : str, 
               order : bool = False):
    """合并指定文件夹下的所有pdf文件

    Args:
        path (str): 指定文件夹, 将需要合并的pdf都存放在这个文件夹当中, 文件夹地址末尾不带\;
        result_file (str): pdf合并完成之后的文件存放地址;
        order (bool, optional): 待合并的pdf是否有先后排序, 如果需要安装一定先后顺序合并，
                                则需要修改指定文件夹下的pdf文件命名，不能用中文，
                                eg.1,2,3... 或者 a,b,c,d...;. Defaults to False.
    """

    import os
    from PyPDF2 import PdfFileReader, PdfFileWriter


    # # 读取指定文件夹下的所有pdf文件
    file_list = os.listdir(path)
    file_list_pdf = list(filter(lambda x: x[-4:].lower() == '.pdf', file_list))  # 只要后缀为.pdf的文件名
    if order == True:  # # 如果需要排序
        file_list_pdf.sort(key=lambda n: int(n[:-4]))  # 对pdf排序，1,2,3,4....
    # # 补全待合并pdf文件地址
    file_list_pdf = [path + '\\' + i for i in file_list_pdf]

    # # 建立一个空白的pdf对象
    merge = PdfFileWriter()

    for i in file_list_pdf:  # 遍历所有pdf
        p1_reader = PdfFileReader(i)  # 读取每个pdf文件
        for j in range(p1_reader.getNumPages()):  # 遍历单个pdf每一页
            merge.addPage(p1_reader.getPage(j))  # 将待合并pdf的每一页存放到空白的对象merge中
    # 写入输出
    with open(result_file, 'wb') as f:
        merge.write(f)


def get_Innermost_file(outer_filename : str, 
                       Innermost_file_suffix : str) -> list:
    """获取文件夹最内层的数据文件，主要用于多层文件嵌套时

    Args:
        outer_filename (str): 最外层文件夹名(地址), 末尾不含\;
        Innermost_file_suffix (str): 最内层数据文件的后缀名, 无.;

    Returns:
        list: 返回指定文件夹下所有指定后缀的文件名
    """

    import os


    files = [outer_filename + '\\' + x for x in os.listdir(outer_filename)]  # 获取第一层文件夹内的文件名，并补全地址
    while True:
        if Innermost_file_suffix.lower() in \
            [x[-1 * len(Innermost_file_suffix):].lower() for x in files]:
            break
        else:
            files = [x + '\\' for x in files]  # 在末尾加上'\\'
            temp = []
            for file in files:
                temp = temp + [file + x for x in os.listdir(file)]
            files = temp
            
    return files

















