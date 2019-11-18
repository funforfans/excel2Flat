 [![License](https://img.shields.io/:license-apache-blue.svg)](https://opensource.org/licenses/Apache-2.0) 
 [![Build Status](https://www.travis-ci.org/funforfans/excel2Flat.svg?branch=master)](https://www.travis-ci.org/funforfans/excel2Flat)
# excel2Flat
将 Excel 配表数据，以 flatbuffers 的形式存储，并将表结构转为 flatbuffers 代码，打包成二进制语言，提供给服务器和客户端调用。

## 执行顺序

- [x] 将 Excel 表结构解析成 flatbuffers 的 fbs 文件

- [x] 通过 flatc 生成目标语言 flatbuffers 代码 (**支持多种语言接口**)

- [x] 将 excel 表数据按 flatbuffers 的结构，将每一个表打包成二进制文件。


## how to use
### 1. install dependence
```
pip install -r requirements.txt
# install flatc source code to binaries
sh build_flatc.sh
```
### 2. python 3.x env(need python3)
> depend on `xlrd` and `flatbuffers`

```
python run.py
```
### 3. binary package(bin use directly)
> depend on  `pyinstaller`

```
sh build_bin.sh
sh exec_data_py.sh
```


