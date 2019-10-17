# -*- coding:utf-8 -*-
# auth:evan xu
# date:2019-10-17

import xlrd
import sys
import os
from common import utils, base


class FbsGenerator(base.Generator):
    """
    生成fbs类
    """

    __row_code = """
table %s {
    %s
}
"""

    __group_code = """
table %s {
    datalist:[%s];
}
"""
    @classmethod
    def clean_directory(cls, target_path):
        """
        
        :param target_path: 
        :return: 
        """
        if not os.path.isdir(target_path):
            os.mkdir(target_path)
        try:
            for root, dirs, files in os.walk(target_path):
                for file in files:
                    path = os.path.join(root, file)
                    os.remove(path)
                    print("清理文件: ", path)
        except:
            print('旧数据清理失败，请关掉已打开的旧文件')
            sys.exit()

    def export_all_excel_to_fbs(self):
        """
        excel到fbs
        :return: 
        """
        excel_root_path = os.path.join(os.getcwd(), self.get_config().get("excel_rootPath"))
        if not excel_root_path:
            print("没有配置excel文件夹的路径，请手动创建一个！")
            sys.exit()
        for root, dirs, files in os.walk(excel_root_path, topdown=True):
            print(root, dirs, files)
            for name in files:
                file_path = os.path.join(root, name)
                if file_path.endswith(self.get_config().get("excel_extension")) and not name.startswith('~'):
                    self.export_excel_to_fbs(file_path)

    def export_excel_to_fbs(self, excel_path):
        """
        
        :param excel_path: 
        :return: 
        """
        # 打开excel，分别将每一个sheet导出fbs
        wb = xlrd.open_workbook(excel_path)
        sheet_count = len(wb.sheet_names())
        for x in range(0, sheet_count):
            sheet = wb.sheet_by_index(x)
            self.export_sheet_to_fbs(sheet)

    def export_sheet_to_fbs(self, sheet):
        """
        excel的sheet导出为fbs
        :param sheet: 
        :return: 
        """
        sheet_name = sheet.name
        if sheet_name.find("|") != -1:
            sheet_name = sheet_name.split("|")[1]
        row_table_name = sheet_name + 'RowData'
        group_table_name = sheet_name
        # check if length of row equals
        header_length = self.get_config().get("header_length")
        if not isinstance(header_length, int):
            print('header_length 不是数字类型')
            print('异常退出')
            sys.exit()
        if not utils.checkRowHeaderLength(sheet, header_length):
            print('表头长度各列不一致, 仔细检查')
            print('异常退出')
            sys.exit()
        variable_dict =  self.load_sheet2_dict(sheet)
        if not variable_dict:
            print('无法获取sheet表单数据，请检查excel表中的%s结构' %sheet_name)
            print('异常退出')
            sys.exit()
        #print(variable_name, data_type, data_type in __support_datatypes)
        # 组合变量定义代码字符串
        variables_str = ''
        for variable in variable_dict:
            data_type = variable_dict[variable]
            variables_str += '    %s:%s;\n' % (variable, data_type)
        variables_str = variables_str.strip(' \t\n\t')
        row_data_table_code_str = self.__row_code % (row_table_name, variables_str)
        # 组合列表代码字符串
        group_data_table_code_str = self.__group_code % (group_table_name, row_table_name)
        # 写入文件
        fbs_root_path = self.get_config().get("output_fbs_rootPath")
        fbs_file_path = os.path.join(os.getcwd(), fbs_root_path + "/" + group_table_name + '.fbs')
        print('生成: ', fbs_file_path)
        write_str = row_data_table_code_str + '\n' + group_data_table_code_str
        with open(fbs_file_path, 'w') as f:
            f.write(write_str)

    @classmethod
    def get_all_fbs_file(cls, root_path):
        """
        
        :param root_path: 
        :return: 
        """
        file_list = []
        for root, dirs, files in os.walk(root_path):
            for file in files:
                file_path = os.path.join(root, file)
                file_list.append(file_path)
        return file_list

    def exe_generate_cmd(self, fbs_file, target_path, language_sign):
        """
        执行生成语句
        :param fbs_file: 
        :param target_path: 
        :param language_sign: 
        :return: 
        """
        # flatc所在目录
        work_root = os.getcwd()
        flatc_path = os.path.join(work_root, self.get_config().get("flat_path"))
        if language_sign == "bins" or language_sign == "fbs" or language_sign == "exec":
            return
        print('生成 {} 代码'.format(language_sign))
        command = '{} --{} -o {} {} --gen-onefile'.format(flatc_path, language_sign, target_path, fbs_file)
        print(command)
        os.system(command)

    def generate_target(self, target_path, language_sign):
        """
        
        :param target_path: 
        :param language_sign: 
        :return: 
        """
        fbs_path_list = self.get_all_fbs_file(self.get_config().get("output_fbs_rootPath"))
        for file_path in fbs_path_list:
            self.exe_generate_cmd(file_path, target_path, language_sign)

    def clean(self):
        """
        清理上次的数据
        :return: 
        """
        # 本工具的根目录
        work_root = os.getcwd()
        lang_types = self.get_config().get("generate_lang_type")
        for lang in lang_types:
            lang_str = "generated_%s" % lang
            lang_root_path = os.path.join(work_root, lang_str)
            FbsGenerator.clean_directory(lang_root_path)

    def run(self):
        """
        执行生成fbs文件
        :return: 
        """
        print('---------------- 清理旧文件 ----------------')
        #self.clean()
        print('---------------- 生成fbs文件, 生成不同语言代码 ----------------')
        self.export_all_excel_to_fbs()
        # 本工具的根目录
        work_root = os.getcwd()
        lang_types = self.get_config().get("generate_lang_type")
        for lang in lang_types:
            lang_str = "generated_%s" %lang
            lang_root_path = os.path.join(work_root, lang_str)
            self.generate_target(lang_root_path, lang)	# 生成Python代码是必须的，因为要用来打包数据
        # 还可以自己扩展，生成指定语言的代码