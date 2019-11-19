# coding=utf-8
import json, os, sys, yaml

class ConfigLoader(object):
    """
    配置加载器
    """
    _config_type_list = ("yaml", "yml", "json")
    @staticmethod
    def get_config_dict(path, config_type="json"):
        """
        配置构造器
        :param path: 
        """
        if not os.path.exists(path):
            print(path, "<-----------配置文件加载失败！请确认配置路径!")
            return
        if config_type == "json":
            return ConfigLoader.load_config_json(path)
        elif config_type == "yml" or "yaml":
            return ConfigLoader.load_config_yml(path)
        else:
            raise("不支持%s 类型的配置文件", config_type)

    @staticmethod
    def load_config_json(path):
        """
        加载json哦配置
        :param path: 
        :return: 
        """
        with open(path, "r") as f:
            try:
                config = json.loads(f.read())
            except:
                print(path, "      <-----------配置加载失败！请确认配置内容是否是标准json格式!")
                sys.exit()
        print(path, "加载成功!")
        return config

    @staticmethod
    def load_config_yml(path):
        """
        加载json哦配置
        :param path: 
        :return: 
        """
        with open(path, "r") as f:
            try:
                cont = f.read()
                config = yaml.load(cont, Loader=yaml.FullLoader)
            except:
                print(path, "      <-----------配置加载失败！请确认配置内容是否是标准yaml格式!")
                sys.exit()
        print(path, "加载成功!")
        return config