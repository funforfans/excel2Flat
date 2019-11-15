# -*- coding:utf-8 -*-
# auth:evan xu
# date:2019-10-17

import xlrd
import sys
import os
from common import utils, base

class BytesGenerator(base.Generator):
    """
    负责生成二进制文件的类
    """

    def get_assign_code(self, mod_name, field_name, field_value, field_type, index):
        if field_type == 'string':
            value_code = "{}{}".format(field_name, index)
            # 只改变首字母大写
            value_code = value_code[0].upper()+value_code[1:]
        else:
            value_code = field_value or 0
        code = "{ModName}.{ModName}Add{FieldName}(builder, {ValueCode})".format(
            ModName = mod_name, FieldName = field_name, ValueCode = value_code)
        return code

    def get_single_data_code(self, mod_name, row_data, index):
        """
        
        :param mod_name: 
        :param row_data: 
        :param index: 
        :return: 
        """
        code = \
        """{VariableCreate}
{ModName}.{ModName}Start(builder)
{AssignCode}
single_data{Index} = {ModName}.{ModName}End(builder)"""

        variable_create_code = ''
        for field in row_data:
            field['field_name'] = field['field_name'][0].upper() + field['field_name'][1:]
            if field['field_type'] == 'string':
                variable_create_code += """{}{} = builder.CreateString("{}")""".format(field['field_name'], index, field['field_value'])
                variable_create_code += '\n'
        assign_code = ''
        for field in row_data:
            assign_code += self.get_assign_code(
                                                mod_name,
                                                field['field_name'],
                                                field['field_value'],
                                                field['field_type'],
                                                index
                                            )
            assign_code += '\n'
        assign_code = assign_code[:-1]
        code = code.format(VariableCreate = variable_create_code, ModName = mod_name, AssignCode = assign_code, Index = index)
        return code

    def get_list_data_code(self, mod_name, single_mod_name, list_data):
        """
        
        :param mod_name: 
        :param single_mod_name: 
        :param list_data: 
        :return: 
        """
        row_count = len(list_data)
        all_assign_code = ''
        index = 0
        for row_data in list_data:
            all_assign_code += self.get_single_data_code(single_mod_name, row_data, index)
            index += 1
            all_assign_code += '\n'
        offset_code = ''
        for index in range(0, row_count):
            data_name = "single_data{}".format(index)
            offset_code += "builder.PrependUOffsetTRelative({})".format(data_name)
            offset_code += '\n'
            code = \
"""
import sys
sys.path.append('../generated_python')
from generated_python import {SingleModName}
from generated_python import {ModName}
import flatbuffers

builder = flatbuffers.Builder(1)

{AllAssignCode}
{ModName}.{ModName}StartDatalistVector(builder, {DataCount})
{OffsetCode}
data_array = builder.EndVector({DataCount})

{ModName}.{ModName}Start(builder)
{ModName}.{ModName}AddDatalist(builder, data_array)
final_data = {ModName}.{ModName}End(builder)
builder.Finish(final_data)
buf = builder.Output()
""".format(
                SingleModName = single_mod_name,
                ModName = mod_name,
                AllAssignCode = all_assign_code,
                DataCount = row_count,
                OffsetCode = offset_code
            )
            return code

    def generate_bytes(self, mod_name, single_mod_name, excel_row_list):
        """
        
        :param mod_name: 
        :param single_mod_name: 
        :param bytes_file_root_path: 
        :param excel_row_list: 
        :return: 
        """
        os.path.realpath(sys.argv[0])
        list_code = self.get_list_data_code(mod_name, single_mod_name, excel_row_list)
        fbs_root_path = self.get_config().get("output_bin_rootPath")
        bytes_file_root_path = os.path.dirname(os.path.abspath(__file__)) + "/" + fbs_root_path
        byte_file_path = os.path.join(bytes_file_root_path, "{}.bytes".format(mod_name))
        byte_file_path = byte_file_path.replace('\\', '/')
        code = """
{ListCode}
with open('{ByteFilePath}', 'wb') as f:
    f.write(buf)
""".format(ListCode = list_code, ByteFilePath = byte_file_path)
        exec(code)
        """
        py_file_name = "generated_python/" + mod_name + "_exec.py"
        excel_root_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), py_file_name)
        print(excel_root_path)
        f=open(excel_root_path, 'w') # 清空文件内容再写
        f.write(code)  # 只能写字符串
        f.close()
        """

    # Bytes 生成代码
    # ================================== Excel 数据读取 ==================================
    @staticmethod
    def get_real_value(data_type, raw_value):
        """
        
        :param data_type: 
        :param raw_value: 
        :return: 
        """
        #print('data_type: ', data_type, 'raw_value:', raw_value)
        if data_type == 'string':
            return str(raw_value or "")
        elif data_type == 'int':
            return int(raw_value or 0)
        elif data_type == 'float':
            return float(raw_value or 0.0)
        else:
            return None

    def read_excel_sheet(self, sheet):
        """
        读取excel配置
        :param sheet: 
        :return: 
        """
        sheet_name = sheet.name
        if sheet_name.find("|") != -1:
            sheet_name = sheet_name.split("|")[1]
        mod_name = sheet_name
        single_mod_name = sheet_name + 'RowData'
        header_length = self.get_config().get("header_length")
        if not utils.checkRowHeaderLength(sheet, header_length):
            print('表头长度各列不一致, 仔细检查')
            print('异常退出')
            sys.exit()
        variable_dict =  self.load_sheet2_dict(sheet)
        if not variable_dict:
            sys.exit()
        # print(variable_name, data_type, data_type in __support_datatypes)
        # 组合变量定义代码字符串
        data_row_count = sheet.nrows
        sheet_row_data_list = []
        header_length = self.get_config().get("header_length")
        if not isinstance(header_length, int):
            print('配置中header_length的类型是%s，这不是数字类型' %type(header_length))
            print('异常退出')
            sys.exit()
        for x in range(header_length, data_row_count):
            row_data = sheet.row(x)
            # 存储每一个字段的字段名，数值，类型
            single_row_data = []
            index = 0
            for variable_name in variable_dict:
                #print(variable_name)
                variable_type = variable_dict[variable_name]
                variable_value = self.get_real_value(variable_type, row_data[index].value)
                # print(variable_name, variable_type, variable_value)
                index += 1
                data_dict = {
                    'field_name': variable_name,
                    'field_value': variable_value,
                    'field_type': variable_type
                }
                single_row_data.append(data_dict)
            sheet_row_data_list.append(single_row_data)
        self.generate_bytes(mod_name, single_mod_name, sheet_row_data_list)

    def generate_excel_data(self, excel_path):
        """
        
        :param excel_path: 
        :return: 
        """
        wb = xlrd.open_workbook(excel_path)
        sheet_count = len(wb.sheet_names())
        for x in range(0, sheet_count):
            sheet = wb.sheet_by_index(x)
            self.read_excel_sheet(sheet)

    def generate_all_excel_byte_data(self):
        """
        
        :return: 
        """
        excel_root_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.get_config().get("excel_rootPath"))
        for root, dirs, files in os.walk(excel_root_path):
            for file in files:
                excel_file_path = os.path.join(root, file)
                if excel_file_path.endswith(self.get_config().get("excel_extension")) and not file.startswith('~'):
                    self.generate_excel_data(excel_file_path)

    def run(self):
        """
        
        :return: 
        """
        print('---------------- 将excel生成flatbuffers二进制数据 ----------------')
        self.generate_all_excel_byte_data()