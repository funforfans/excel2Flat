# coding=utf-8

from common import loader

class Generator(object):
    """
    生成器的基类
    """
    __config={}
    def __init__(self, path):
        """
        初始化
        """
        self.__config = loader.load_config(path)

    def get_config(self):
        """
        返回配置
        :return: 
        """
        return self.__config

    def run(self):
        """
        执行
        :return: 
        """

    def load_sheet2_dict(self, sheet):
        """
        从excel加载各列到字典中
        :param sheet_name: 
        :return: 
        """
        variable_dict = {}
        data_type_list = sheet.row(1)
        field_name_list = sheet.row(2)
        for i in range(len(field_name_list)):
            variable_name = field_name_list[i].value
            # 这里需要类型转换
            data_type = data_type_list[i].value
            if not data_type:
                continue
            if variable_name in variable_dict:
                print('存在相同的字段名: ', variable_name)
                print('异常退出')
                return
            # 如果是可替换的数据类型
            replace_dict = self.__config.get("replace_dict")
            support_datatypes = self.__config.get("support_datatypes")
            if replace_dict.get(data_type):
                data_type = replace_dict[data_type]
            if not data_type in support_datatypes:
                print('字段', variable_name, '的数据类型', data_type,'不在支持的列表中')
                print('异常退出')
                return
            variable_dict[variable_name] = data_type
        return variable_dict


