# -*- coding: utf-8 -*-
import xlwt
import json

def get_excel(filename): 
    # 创建excel工作表
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('sheet1')
     
    # 设置表头
    #worksheet.write(0, 0, label='NAME')
    #worksheet.write(0, 1, label='LEN')
    #worksheet.write(0, 2, label='ID')
    #worksheet.write(0, 3, label='OTHER')
    worksheet.write(0, 0, label='name')
    worksheet.write(0, 1, label='age')
     
     
    # 读取json文件
    #with open('test.json', 'r') as f:
    #data = json.load(f)
    data = [{"name":"xiaoming1111111111111111", "age": "11"}, {"name":"xiaoxiao22222222222222222", "age": "12"}, {"name":"xiaohong333333333333333333333333333", "age": "13"}]
     
    # 将json字典写入excel
    # 变量用来循环时控制写入单元格，感觉有更好的表达方式
    #val1 = 1
    #val2 = 1
    #al3 = 1
    # #val4 = 1
    # for list_item in data:
        # for key, value in list_item.items():
            # if key == "NAME":
                # worksheet.write(val1, 0, value)
            # elif key == "LEN":
                # worksheet.write(val2, 1, value)
            # elif key == "ID":
                # worksheet.write(val3, 2, value)
            # elif key == "OTHER":
                # worksheet.write(val4, 3, value)
            # else:
                # pass
    for i, sub in enumerate(data, 1):
        worksheet.write(i, 0, sub['name'])
        worksheet.write(i, 1, sub['age'])
     
    # 保存
    workbook.save(filename)