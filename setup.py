"""
setup.py文件配置参照：
https://zhuanlan.zhihu.com/p/276461821

打包命令：python setup.py sdist bdist_wheel，生成gz和whl文件
发布到PYPI：python3 -m twine upload dist/*
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding='UTF-8') as fh:
      long_des1 = fh.read()
with open("VERSIONUPDATE.md", "r", encoding='UTF-8') as fh1:
      long_des2 = fh1.read()
long_des = long_des1 + "\n\n" + long_des2


print(find_packages())
setup(name="MeteoPy",
      version="0.0.1",
      url="https://gitee.com/MeteoTop/MeteoPy",
      description="存放一些在科研过程中实用的python函数，主要针对大气科学学科，包括绘图、数据处理、文档处理等。",
      py_modules=["MeteoPy"],  # 需要打包的python文件列表
      keywords="大气科学 气象绘图 数据处理",
      author="Shanchuan Xiao",
      author_email="xsc_nhno@foxmail.com",
      packages=find_packages(),
      install_requires=[
            'cnmaps==1.1.1',  # 会同时安装numpy、pandas、netCDF4、Shapely、cartopy、matplotlib等库
            ],
      long_description=long_des,
      long_description_content_type="text/markdown",
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        ])
