[![Build Status](https://www.travis-ci.org/xuyiwenak/excel2Flat.svg?branch=master)](https://www.travis-ci.org/xuyiwenak/excel2Flat)
# excel2Flat
将 Excel 配表数据，以 flatbuffers 的形式存储，并将表结构转为 flatbuffers 代码，打包成二进制语言，提供给服务器和客户端调用。

## 执行顺序

- [x] 将 Excel 表结构解析成 flatbuffers 的 fbs 文件

- [x] 通过 flatc 生成目标语言 flatbuffers 代码 (**支持多种语言接口**)

- [x] 将 excel 表数据按 flatbuffers 的结构，将每一个表打包成二进制文件。


## 如何使用
```
cd Excel2Flat
# 这个工具用到的Python是 python3.7.x
python run.py
```
> 工具用到了`xlrd`和`flatbuffers`，如果运行报错，提示没有安装这两个模块，需要先使用pip3安装
