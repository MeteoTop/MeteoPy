# 测试DataPro文件夹下的PrePro.py

## 1. 测试heavy_sampling_method()函数


```python
import pandas as pd
from MeteoPy import heavy_sampling_method
```


```python
# # 查看测试数据
test_file = '../TestData/test-30min.xlsx'
test_data = pd.read_excel(test_file, index_col=0)
test_data
```

**output:**

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>DR</th>
      <th>UR</th>
      <th>DLR</th>
      <th>ULR</th>
    </tr>
    <tr>
      <th>TIMESTAMP</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2017-04-01 12:00:00</th>
      <td>930.000000</td>
      <td>126.400000</td>
      <td>288.900000</td>
      <td>484.400000</td>
    </tr>
    <tr>
      <th>2017-04-01 12:30:00</th>
      <td>915.066667</td>
      <td>123.993333</td>
      <td>290.366667</td>
      <td>490.270000</td>
    </tr>
    <tr>
      <th>2017-04-01 13:00:00</th>
      <td>909.866667</td>
      <td>123.683333</td>
      <td>291.906667</td>
      <td>501.396667</td>
    </tr>
    <tr>
      <th>2017-04-01 13:30:00</th>
      <td>891.800000</td>
      <td>121.626667</td>
      <td>292.163333</td>
      <td>510.653333</td>
    </tr>
    <tr>
      <th>2017-04-01 14:00:00</th>
      <td>845.766667</td>
      <td>116.406667</td>
      <td>292.193333</td>
      <td>516.360000</td>
    </tr>
    <tr>
      <th>2017-04-01 14:30:00</th>
      <td>773.556667</td>
      <td>106.466667</td>
      <td>293.266667</td>
      <td>515.576667</td>
    </tr>
    <tr>
      <th>2017-04-01 15:00:00</th>
      <td>686.596667</td>
      <td>96.480000</td>
      <td>295.806667</td>
      <td>516.000000</td>
    </tr>
    <tr>
      <th>2017-04-01 15:30:00</th>
      <td>585.230000</td>
      <td>83.264667</td>
      <td>296.546667</td>
      <td>510.566667</td>
    </tr>
    <tr>
      <th>2017-04-01 16:00:00</th>
      <td>477.170000</td>
      <td>70.346000</td>
      <td>298.900000</td>
      <td>502.723333</td>
    </tr>
    <tr>
      <th>2017-04-01 16:30:00</th>
      <td>365.630000</td>
      <td>56.013000</td>
      <td>297.413333</td>
      <td>491.070000</td>
    </tr>
    <tr>
      <th>2017-04-01 17:00:00</th>
      <td>246.576667</td>
      <td>37.756000</td>
      <td>297.253333</td>
      <td>475.110000</td>
    </tr>
    <tr>
      <th>2017-04-01 17:30:00</th>
      <td>124.262667</td>
      <td>15.039333</td>
      <td>295.976667</td>
      <td>458.620000</td>
    </tr>
    <tr>
      <th>2017-04-01 18:00:00</th>
      <td>41.275000</td>
      <td>10.658000</td>
      <td>293.276667</td>
      <td>444.156667</td>
    </tr>
    <tr>
      <th>2017-04-01 18:30:00</th>
      <td>12.676706</td>
      <td>6.802412</td>
      <td>293.643333</td>
      <td>432.466667</td>
    </tr>
  </tbody>
</table>


### 1.1 第一类小时平均

```python
# # 测试函数
start_time = '2017-04-01 12:00:00'
end_time = '2017-04-01 19:00:00'
heavy_sampling_method(test_data, start_time, end_time, '1h', 'mean', type=0)
```

    DatetimeIndex(['2017-04-01 12:00:00', '2017-04-01 13:00:00',
                   '2017-04-01 14:00:00', '2017-04-01 15:00:00',
                   '2017-04-01 16:00:00', '2017-04-01 17:00:00',
                   '2017-04-01 18:00:00', '2017-04-01 19:00:00'],
                  dtype='datetime64[ns]', freq='H')
    重抽样计算:2017-04-01 12:00:00  用时:0.013964653015136719s
    重抽样计算:2017-04-01 13:00:00  用时:0.016954660415649414s
    重抽样计算:2017-04-01 14:00:00  用时:0.019945859909057617s
    重抽样计算:2017-04-01 15:00:00  用时:0.024930715560913086s
    重抽样计算:2017-04-01 16:00:00  用时:0.026925086975097656s
    重抽样计算:2017-04-01 17:00:00  用时:0.02991652488708496s
    重抽样计算:2017-04-01 18:00:00  用时:0.03392171859741211s
    重抽样计算:2017-04-01 19:00:00  用时:0.03690004348754883s

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>DR</th>
      <th>UR</th>
      <th>DLR</th>
      <th>ULR</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2017-04-01 12:00:00</th>
      <td>930.000000</td>
      <td>126.400000</td>
      <td>288.900000</td>
      <td>484.400000</td>
    </tr>
    <tr>
      <th>2017-04-01 13:00:00</th>
      <td>912.466667</td>
      <td>123.838333</td>
      <td>291.136667</td>
      <td>495.833333</td>
    </tr>
    <tr>
      <th>2017-04-01 14:00:00</th>
      <td>868.783333</td>
      <td>119.016667</td>
      <td>292.178333</td>
      <td>513.506667</td>
    </tr>
    <tr>
      <th>2017-04-01 15:00:00</th>
      <td>730.076667</td>
      <td>101.473333</td>
      <td>294.536667</td>
      <td>515.788333</td>
    </tr>
    <tr>
      <th>2017-04-01 16:00:00</th>
      <td>531.200000</td>
      <td>76.805333</td>
      <td>297.723333</td>
      <td>506.645000</td>
    </tr>
    <tr>
      <th>2017-04-01 17:00:00</th>
      <td>306.103333</td>
      <td>46.884500</td>
      <td>297.333333</td>
      <td>483.090000</td>
    </tr>
    <tr>
      <th>2017-04-01 18:00:00</th>
      <td>82.768833</td>
      <td>12.848667</td>
      <td>294.626667</td>
      <td>451.388333</td>
    </tr>
    <tr>
      <th>2017-04-01 19:00:00</th>
      <td>12.676706</td>
      <td>6.802412</td>
      <td>293.643333</td>
      <td>432.466667</td>
    </tr>
  </tbody>
</table>


### 1. 2第二类小时平均

```python
heavy_sampling_method(test_data, start_time, end_time, '1h', 'mean', type=1)
```

    DatetimeIndex(['2017-04-01 12:00:00', '2017-04-01 13:00:00',
                   '2017-04-01 14:00:00', '2017-04-01 15:00:00',
                   '2017-04-01 16:00:00', '2017-04-01 17:00:00',
                   '2017-04-01 18:00:00', '2017-04-01 19:00:00'],
                  dtype='datetime64[ns]', freq='H')
    重抽样计算:2017-04-01 13:00:00  用时:0.006975889205932617s
    重抽样计算:2017-04-01 14:00:00  用时:0.01096034049987793s
    重抽样计算:2017-04-01 15:00:00  用时:0.013952016830444336s
    重抽样计算:2017-04-01 16:00:00  用时:0.01598215103149414s
    重抽样计算:2017-04-01 17:00:00  用时:0.0179443359375s
    重抽样计算:2017-04-01 18:00:00  用时:0.020936250686645508s
    重抽样计算:2017-04-01 19:00:00  用时:0.02293086051940918s

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>DR</th>
      <th>UR</th>
      <th>DLR</th>
      <th>ULR</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2017-04-01 13:00:00</th>
      <td>922.533333</td>
      <td>125.196667</td>
      <td>289.633333</td>
      <td>487.335000</td>
    </tr>
    <tr>
      <th>2017-04-01 14:00:00</th>
      <td>900.833333</td>
      <td>122.655000</td>
      <td>292.035000</td>
      <td>506.025000</td>
    </tr>
    <tr>
      <th>2017-04-01 15:00:00</th>
      <td>809.661667</td>
      <td>111.436667</td>
      <td>292.730000</td>
      <td>515.968333</td>
    </tr>
    <tr>
      <th>2017-04-01 16:00:00</th>
      <td>635.913333</td>
      <td>89.872333</td>
      <td>296.176667</td>
      <td>513.283333</td>
    </tr>
    <tr>
      <th>2017-04-01 17:00:00</th>
      <td>421.400000</td>
      <td>63.179500</td>
      <td>298.156667</td>
      <td>496.896667</td>
    </tr>
    <tr>
      <th>2017-04-01 18:00:00</th>
      <td>185.419667</td>
      <td>26.397667</td>
      <td>296.615000</td>
      <td>466.865000</td>
    </tr>
    <tr>
      <th>2017-04-01 19:00:00</th>
      <td>26.975853</td>
      <td>8.730206</td>
      <td>293.460000</td>
      <td>438.311667</td>
    </tr>
  </tbody>
</table>


## 2. 测试WRF_Chem_getvars()类


```python
import os
import xarray as xr
from MeteoPy import WRF_Chem_getvars
```

### 2.1 查看数据文件夹内容
```python
path = '../TestData/WRF-Chem_out/'
file_list = os.listdir(path)
file_list
```
**output:**

    ['CCTM_SA_ACONC_v532_gcc_190316_20210102.nc',
     'CCTM_SA_ACONC_v532_gcc_190316_20210103.nc']

### 2.2 测试类


```python
path = '../TestData/WRF-Chem_out/'
which = ['O3', 'PM2.5']
ncfile = '../TestData/WRF-Chem_out/202101_O3_PM25.nc'
WRF_Chem_getvars(path, which, ncfile)
```
**output:**

    ../TestData/WRF-Chem_out//CCTM_SA_ACONC_v532_gcc_190316_20210102.nc: 合并完成！
    ../TestData/WRF-Chem_out//CCTM_SA_ACONC_v532_gcc_190316_20210103.nc: 合并完成！
    合并完成！

### 2.3 再次查看数据文件夹内容


```python
# # 查看是否生成合并后的数据
path = '../TestData/WRF-Chem_out/'
file_list = os.listdir(path)
file_list
```

**output:**


    ['202101_O3_PM25.nc',
     'CCTM_SA_ACONC_v532_gcc_190316_20210102.nc',
     'CCTM_SA_ACONC_v532_gcc_190316_20210103.nc']

### 2.4 查看202101_O3_PM25.nc，是否修改维度成功


```python
xr.open_dataset(ncfile)
```

![png](./PreProTest-image/output.png)