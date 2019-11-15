# coding=utf-8
import json, os, sys

def load_config(path):
    """
    加载json哦配置
    :param path: 
    :return: 
    """
    if not os.path.exists(path):
        print(path, "<-----------配置文件加载失败！请确认配置路径!")
        sys.exit()
    with open(path, "r") as f:
        try:
            config = json.loads(f.read())
        except:
            print(path, "      <-----------配置加载失败！请确认配置内容!")
            sys.exit()
    print(path, "加载成功!")
    return config
