# 测试DataPro文件夹下的Statistic.py

## 1. 通用测试数据


```python
import numpy as np

data1 = np.array([[1, 2, 3, 4, 5], [2, 3, 4, 5, 6], [2, 3, 4, 5, 6]])
data2 = np.array([[2, 3, 1, 5, 7], [3, 1, 4, 6, 3], [8, 3, 4, 1, 2]])
print('data1: ', data1, sep='\n', end='\n\n')
print('data2: ', data2, sep='\n', end='\n\n')
print('data1 - data2: ', data1 - data2, sep='\n')
```

**output:**

    data1: 
    [[1 2 3 4 5]
     [2 3 4 5 6]
     [2 3 4 5 6]]
    
    data2: 
    [[2 3 1 5 7]
     [3 1 4 6 3]
     [8 3 4 1 2]]
    
    data1 - data2: 
    [[-1 -1  2 -1 -2]
     [-1  2  0 -1  3]
     [-6  0  0  4  4]]



## 2. 测试RMSE()函数


```python
from MeteoPy import RMSE
```


### 2.1 列与列axis=0

```python
RMSE(data1, data2, axis=0)
```

**output:**


    array([3.55902608, 1.29099445, 1.15470054, 2.44948974, 3.10912635])

### 2.2 行与行axis=1


```python
RMSE(data1, data2, axis=1)
```

**output:**


    array([1.4832397 , 1.73205081, 3.68781778])



## 3. 测试MAE()函数


```python
from MeteoPy import MAE
```

### 3.1 列与列axis=0

```python
MAE(data1, data2, axis=0)
```

**output:**


    array([2.66666667, 1.        , 0.66666667, 2.        , 3.        ])

### 3.2 行与行axis=1


```python
MAE(data1, data2, axis=1)
```

**output:**


    array([1.4, 1.4, 2.8])



## 4. 测试contrast()函数


```python
from MeteoPy import contrast
```

### 3.1 列与列axis=0


```python
contrast(data1, data2, axis=0)
```

**output:**

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>MAE</th>
      <th>RMSE</th>
      <th>R</th>
      <th>P-value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2.666667</td>
      <td>3.559026</td>
      <td>0.628619</td>
      <td>0.567241</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1.000000</td>
      <td>1.290994</td>
      <td>-0.5</td>
      <td>0.666667</td>
    </tr>
    <tr>
      <th>2</th>
      <td>0.666667</td>
      <td>1.154701</td>
      <td>1.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2.000000</td>
      <td>2.449490</td>
      <td>-0.327327</td>
      <td>0.787704</td>
    </tr>
    <tr>
      <th>4</th>
      <td>3.000000</td>
      <td>3.109126</td>
      <td>-0.981981</td>
      <td>0.121038</td>
    </tr>
  </tbody>
</table>


### 4.2 行与行axis=1


```python
contrast(data1, data2, axis=1)
```

**output:**

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>MAE</th>
      <th>RMSE</th>
      <th>R</th>
      <th>P-value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1.4</td>
      <td>1.483240</td>
      <td>0.787839</td>
      <td>0.113502</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1.4</td>
      <td>1.732051</td>
      <td>0.435194</td>
      <td>0.463918</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2.8</td>
      <td>3.687818</td>
      <td>-0.819288</td>
      <td>0.089676</td>
    </tr>
  </tbody>
</table>

