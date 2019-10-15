# -*- coding:utf-8 -*-
import xlrd
import sys
import os
from common import utils, const


__excel_extension = 'xlsx'

__support_datatypes = ['string', 'int', 'float', 'byte','bool']
# 直接做替换用的字符串
__replace_dict = {"boolean": "bool",
                  "String": "string",
                  "int[]": "string",
                  }

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

def __clean_directory(target_path):
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



def __export_all_excel_to_fbs():
    for root, dirs, files in os.walk(excel_root_path, topdown=True):
        for name in files:
            print(name)
            file_path = os.path.join(root, name)
            if file_path.endswith(__excel_extension) and not name.startswith('~'):
                __export_excel_to_fbs(file_path)

def __export_excel_to_fbs(excel_path):
    # 打开excel，分别将每一个sheet导出fbs
    wb = xlrd.open_workbook(excel_path)
    sheet_count = len(wb.sheet_names())
    sheet1 = wb.sheet_by_index(0)
    for x in range(0, sheet_count):
        sheet = wb.sheet_by_index(x)
        __export_sheet_to_fbs(sheet)

def __export_sheet_to_fbs(sheet):
    """
    excel的sheet导出为fbs
    :param sheet: 
    :return: 
    """
    variable_dict = {}
    sheet_name = sheet.name
    print(sheet_name.find("|"))
    if sheet_name.find("|") != -1:
        print(sheet_name)
        sheet_name = sheet_name.split("|")[1]
    row_table_name = sheet_name + 'RowData'
    group_table_name = sheet_name
    client_or_server = sheet.row(0)
    data_type_list = sheet.row(1)
    field_name_list = sheet.row(2)
    field_des = sheet.row(3)
    # check if length of row equals
    if not utils.__checkRowHeaderLength(sheet, const.header_length):
        print('表头长度各列不一致, 仔细检查')
        print('异常退出')
        sys.exit()
    for i in range(len(field_name_list)):
        variable_name = field_name_list[i].value
        # 这里需要类型转换
        data_type = data_type_list[i].value
        if not data_type:
            continue
        if variable_name in variable_dict:
            print('存在相同的字段名: ', variable_name)
            print('异常退出')
            sys.exit()
        # 如果是可替换的数据类型
        if __replace_dict.get(data_type):
            data_type = __replace_dict[data_type]
        if not data_type in __support_datatypes:
            print('字段', variable_name, '的数据类型', data_type,'不在支持的列表中')
            print('异常退出')
            sys.exit()
        variable_dict[variable_name] = data_type
        #print(variable_name, data_type, data_type in __support_datatypes)
    # 组合变量定义代码字符串
    variables_str = ''
    for variable in variable_dict:
        data_type = variable_dict[variable]
        variables_str += '    %s:%s;\n' % (variable, data_type)
    variables_str = variables_str.strip(' \t\n\t')
    row_data_table_code_str = __row_code % (row_table_name, variables_str)
    # 组合列表代码字符串
    group_data_table_code_str = __group_code % (group_table_name, row_table_name)
    # 写入文件
    fbs_file_path = os.path.join(fbs_root_path, group_table_name + '.fbs')
    print('生成: ', fbs_file_path)
    write_str = row_data_table_code_str + '\n' + group_data_table_code_str
    with open(fbs_file_path, 'w') as f:
        f.write(write_str)


def __get_all_fbs_file(root_path):
    file_list = []
    for root, dirs, files in os.walk(root_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_list.append(file_path)
    return file_list


def __generate_target_file(fbs_file, target_path, language_sign):
    command = '{} --{} -o {} {} --gen-onefile'.format(flatc_path, language_sign, target_path, fbs_file)
    os.system(command)


def __generate_target(target_path, language_sign):
    print('生成 {} 代码'.format(language_sign))
    fbs_path_list = __get_all_fbs_file(fbs_root_path)
    for file_path in fbs_path_list:
        __generate_target_file(file_path, target_path, language_sign)


def __clean():
    __clean_directory(fbs_root_path)
    __clean_directory(bytes_root_path)
    __clean_directory(python_root_path)
    __clean_directory(csharp_root_path)
    __clean_directory(go_root_path)
    __clean_directory(rust_root_path)


# 本工具的根目录
work_root = os.getcwd()

# flatc.exe所在目录
flatc_path = os.path.join(work_root, 'flatc/flatc')

# 存放excel的目录
excel_root_path = os.path.join(work_root, 'excel')

# 存放excel生成的flatbuffers二进制文件的目录
bytes_root_path = os.path.join(work_root, 'generated_bytes')

# 生成的 fbs 文件的目录
fbs_root_path = os.path.join(work_root, 'generated_fbs')

# fbs 生成的 python 代码目录
python_root_path = os.path.join(work_root, 'generated_python')

# fbs 生成的 c# 代码目录
csharp_root_path = os.path.join(work_root, 'generated_csharp')

# fbs 生成的 go 代码目录
go_root_path = os.path.join(work_root, 'generated_go')

# fbs 生成的 rust 代码目录
rust_root_path = os.path.join(work_root, 'generated_rust')

def run():
    print('---------------- 清理旧文件 ----------------')
    __clean()
    print('---------------- 生成fbs文件, 生成不同语言代码 ----------------')
    __export_all_excel_to_fbs()
    __generate_target(python_root_path, 'python')	# 生成Python代码是必须的，因为要用来打包数据
    __generate_target(csharp_root_path, 'csharp')
    __generate_target(go_root_path, 'go')
    __generate_target(rust_root_path, 'rust')
    # 还可以自己扩展，生成指定语言的代码