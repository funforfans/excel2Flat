# coding=utf-8

def checkRowHeaderLength(sheet, headerLength=4):
    """
    检查表头的几列是否对应
    :param sheet: 
    :return: 
    """
    a = []
    for i in range(headerLength):
        a.append(len(sheet.row(i)))
    b = list(set(a))
    return True if len(b) == 1 else False