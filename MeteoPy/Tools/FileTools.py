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


def get_all_file(target_path : str, 
                 file_suffix : str = None, 
                 match_case : bool = True) -> list:
    """获取文件夹内所有指定后缀的文件，包括所有嵌套文件夹内的文件

    Args:
        target_path (str): 最外层文件夹名(地址), 末尾不含\
        file_suffix (str, optional): 文件后缀名，含.. Defaults to None.
        match_case (str, optional): 是否区分你大小写.. Defaults to True.

    Returns:
        list: 返回指定文件夹下所有指定后缀的文件名
    """

    import os


    paths = [target_path + '/' + x for x in os.listdir(target_path)]  # 获取第一层文件夹内的文件名，并补全地址
    res = []  # 存储结果
    for path in paths:
        if os.path.isdir(path):
            temp_res = get_all_file(path, file_suffix)
            res.extend(temp_res)
        else:
            if file_suffix == None:
                res.append(path)
            else:
                if match_case:
                    if path[-1 * len(file_suffix):] == file_suffix:
                        res.append(path)
                else:
                    if path[-1 * len(file_suffix):].lower() == file_suffix.lower():
                        res.append(path)
                
    return res


def search_str(target_path : str, 
               target_str : str, 
               match_case : bool = True,
               target_suffix : str = None, 
               output_type : str = 'console'):
    """搜索文件夹下所有文件，查找指定内容

    Args:
        target_path (str): 目标文件夹
        target_str (str): 目标字符串
        match_case (str, optional): 是否区分你大小写.. Defaults to False.
        target_suffix (str, optional): 目标文件后缀名. Defaults to True.
        output_type (str, optional): print输出显示位置. Defaults to console.

    注意：output_type参数默认未控制台输出，查询结果可高亮显示，并且可将输出存为文本。
         但在非控制台输出时，不能显示颜色，比如jupyter输出。
         非控制台输出时，也可高亮显示，但是将输出存为文本包含颜色控制语句。

         "console"和"unconsole"冲突，如果在同一个脚本中，先运行了console，则后面的unconsole
         将会失去高亮显示作用.
    """

    import os


    if os.path.isdir(target_path):
        all_target_file = get_all_file(target_path, target_suffix, match_case)
    else:
        all_target_file = [target_path]

    for file in all_target_file:
        f = open(file, 'r', encoding='UTF-8')
        lines = f.readlines()  # 读取所有行
        for i in range(len(lines)):
            if match_case:
                temp1 = target_str
                temp2 = lines[i]
            else:
                temp1 = target_str.lower()
                temp2 = lines[i].lower()

            if temp1 in temp2:
                if output_type == 'console':
                    from colorama import Fore, init

                    init(autoreset=True)
                    print(Fore.MAGENTA + file, end=':')
                    print(Fore.GREEN + str(i + 1), end=':')
                elif output_type == 'unconsole':
                    print('\033[35m' + file + '\033[0m', end=':')
                    print('\033[32m' + str(i + 1) + '\033[0m', end=':')
                else:
                    raise Exception("Invalid key: 'output_type' is only console or unconsole")
                num_len = 0
                for j in temp2.split(temp1):
                    print(lines[i][num_len:(num_len + len(j))], end='')
                    num_len = num_len + len(j)
                    # # lines[i]为字符串，所以在最后一个元素的时候，
                    # # 也不存在索引越界的情况，超过范围的索引返回空值''
                    if output_type == 'console':
                        print(Fore.RED + lines[i][num_len:(num_len + len(temp1))], end='')
                    elif output_type == 'unconsole':
                        print('\033[31m' + lines[i][num_len:(num_len + len(temp1))] + '\033[0m', end='')
                    num_len = num_len + len(temp1)
        f.close()

















