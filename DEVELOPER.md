# 开发者说明

我们尝试将一些在科研中经常使用到的python程序封装成`函数`或者`类`，方便下次使用。如果有志同道合的朋友，愿意为本开源函数库做出贡献，请仔细阅读本部分内容。

## 函数库编写规范

### 程序书写规范

在程序书写过程中，应善用`空格`，提高程序的可读性。

一般，变量、运算符，逗号等后都用一个空格与其他内容分隔；

### 函数/类说明文字

```python
def Function(var1 : str, 
             var2 : int, 
             var3 : float, 
             var4 : list = [1, 2, 3], 
             var5 : dict = {'a':1, 'b':2, 'c':3}, 
             *var6, 
             **var7
             ) -> str:
    """_summary_

    Args:
        var1 (str): _description_
        var2 (int): _description_
        var3 (float): _description_
        var4 (list, optional): _description_. Defaults to [1, 2, 3].
        var5 (_type_, optional): _description_. Defaults to {'a':1, 'b':2, 'c':3}.

    Returns:
        str: _description_
    """

	"""
        >>> 变量表中，var1-3为定位参数，使用函数时，传参位置不能变，或使用关键字传参
        >>> var4-5为默认值参数，在使用函数时，可以不传参，此时将使用默认值
        >>> var6-7为不参参数，其中var6为不定元组，var7为不定字典
    """
    
    # # 如何对字典类型的可选参数进行初始化
    # # 使用户使用时只需指定修改的参数即可，不用将所有参数都写上
    import sys
	sys.path.append('../../')  # 将MeteoPy目录放入搜索目录
    from Tools.FunVarDefault import dict_default
    
    # # 处理var5默认值问题
    var5_default = {'a':1, 'b':2, 'c':3}  # 指定var5的默认值
    if isinstance(var5, dict):
        var5 = dict_default(var5, var5_default)  # 对var5设置默认值，用户指定的值不变
    
    ......

    return res
```

+ 明确指出各个参数的类型，及其描述。`类型注解`仅适用于**3.6**及以后版本的python，**这种类型和变量注解实际上只是一种类型提示，对运行实际上是没有影响的**；
+ 解释`dict默认值设置`：若用户输入从`var5={'a'=3}`，则在函数中赋予默认值之后，`var5={'a':3, 'b':2, 'c':3}`；

### 程序中的注释

+ 注释一般单行存放，或放于行末；

+ 单行注释应为对其下方的多行程序的整体概况，使用`双#`，＃间用空格隔开。并且单行注释前应空一行；

+ 行末注释应为改行程序的概况，使用`单#`，前面两个空格，后面一个空格；

  ```
  # # 单行注释
  var1 = 1  # 行末注释
  var2 = 2
  
  # # 单行注释 
  ```

