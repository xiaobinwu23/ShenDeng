#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 对已经存在的Excel表进行关键字过滤。
import tkinter.messagebox
import tkinter.filedialog
import xlwt
import xlrd
import os
import re

# --------------读取Excel表-----------
def read():
    default_dir = "默认路径"
    fname = tkinter.filedialog.askopenfilename(title=u'选择Excel文件XBW', initialdir=(os.path.expanduser((default_dir))))
    b = os.path.split(fname)
    hz = re.split('\.', b[1])[1]
    if hz != "xls" and hz != "xlsx":
        print("选择的文件错误！")
        return
    dic_list = []   # 保存写入的数据
    book = xlrd.open_workbook(fname)
    sheet0 = book.sheet_by_index(0)
    nrows = sheet0.nrows
    for i in range(nrows):
        data = sheet0.row_values(i)
        tra = (data[0], data[1])
        dic_list.append(tra)
    QX_write(dic_list, b)

# ------------根据关键字过滤，并写入Excel表-----------
def QX_write(dic_list, path):
    book2 = xlwt.Workbook('utf-8')
    sheet2 = book2.add_sheet("清洗后的技能点")
    dic = {}
    # 要筛选的关键字
    keyword = ['Eclipse', 'Java', 'PHP', '逻辑', '编程', '系统设计', '需求分析', 'Javascript', '面向对象', '设计模式', '代码书写', 'Oracle', 'UML', 'Velocity', 'SQL', '数据库', 'HTML', 'C#', 'Linux', '.NET', 'MVC', 'Web', 'MySQL', '网站', '软件设计']
    for key in keyword:
        sum = 0
        for jnd in dic_list:
            IsExist = re.search(key, jnd[0], re.IGNORECASE)  # 对大小写不敏感
            if IsExist:
                sum += int(jnd[1])
        dic[key] = sum
    for d in dic:   # 去掉包含项的个数
        for i in dic:
            if d.lower() in i.lower() and d != i:
                dic[d] = dic[d] - dic[i]
    li_dic = sorted(dic.items(), key=lambda item: item[1], reverse=True) # 排序
    k = 1
    for ld in li_dic:   # 写入Excel表
        sheet2.write(k, 0, ld[0])
        sheet2.write(k, 1, ld[1])
        k += 1
    SavePath = path[0]+"\清洗后-"+path[1]
    if os.path.exists(SavePath): # 如果该文件已存在，则删除原文件。
        os.remove(SavePath)
    book2.save(SavePath)

if __name__ == "__main__":
    read()