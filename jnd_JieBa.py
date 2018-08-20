#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 获取高频词汇
import xlrd
import xlwt
import os
import tkinter.filedialog
import jieba.analyse

default = "默认路径"
fname = tkinter.filedialog.askopenfilename(title=u'选择Excel文件XBW', initialdir=(os.path.expanduser((default))))
book = xlrd.open_workbook(fname)
sheet0 = book.sheet_by_index(0)
nrow = sheet0.nrows

mstring = ""
for i in range(1, nrow):
    data = sheet0.row_values(i)
    for j in range(int(data[1])):
        mstring = mstring + data[0] + ","

gjz = jieba.analyse.extract_tags(mstring.lower(), 100)
print(gjz)
