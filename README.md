# PyLib
在此仓库中将存放一些我们在科研过程中实用的python脚本，主要针对大气科学学科。

## 脚本规范
​        我们尝试将一些在科研中经常使用到的python脚本封装成`函数`或者`类`，方便下次使用。因此本部分对上传脚本的格式做出如下规范：

### 程序书写规范

​         在程序书写过程中，应善用`空格`，提高程序的可读性。一般变量后都用一个空格与其他变量分隔；

### 函数/类说明文字

```python
def Function(var1 : str, 
             var2 : int, 
             var3 : float, 
             var4 : list = [1, 2, 3], 
             var5 : dict = {'a':4}, 
             *var6, 
             **var7
             ) -> str:
    """_summary_

    Args:
        var1 (str): _description_
        var2 (int): _description_
        var3 (float): _description_
        var4 (list, optional): _description_. Defaults to [1, 2, 3].
        var5 (_type_, optional): _description_. Defaults to {'a':4}.

    Returns:
        str: _description_
    """


    # # 变量表中，var1-3为定位参数，使用函数时，传参位置不能变，或使用关键字传参
    # # var4-5为默认值参数，在使用函数时，可以不传参，此时将使用默认值
    # # var6-7为不参参数，其中var6为不定元组，var7为不定字典

    ......

    return res
```

+ 明确指出各个参数的类型，及其描述。`类型注解`仅适用于**3.6**及以后版本的python，**这种类型和变量注解实际上只是一种类型提示，对运行实际上是没有影响的**；

### 脚本中的注释

+ 注释一般单行存放，或放于行末；

+ 单行注释应为对其下方的多行程序的整体概况，使用`双#`，＃间用空格隔开。并且单行注释前应空一行；

+ 行末注释应为改行程序的概况，使用`单#`，前面两个空格，后面一个空格；

  ```
  # # 单行注释
  var1 = 1  # 行末注释
  var2 = 2
  
  # # 单行注释 
  ```

  







