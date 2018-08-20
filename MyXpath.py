#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
from lxml import html   # xpath库。
import re   # 正则库
import os   # 系统库
import xlwt  # 文件的输出操作。
import xlrd  # 文件的写入操作。

#<editor-fold desc="***爬页面***"
# 把指定 url 的网页内容输出到指定 file。
# 并返回 html类型的 网页内容。
def Get_page(url, file):
    page = requests.get(url)
    with open(file, "w", encoding='utf-8') as f:
        f.write(page.text)
    tree = html.fromstring(page.text)
    return tree
#</editor-fold
#<editor-fold desc="***爬内容***"
# 通过指定 str_xpath 的表达式对 html类型的 tree 进行筛选，并输出到Excel表格里。
# 并返回 list类型的 筛选结果。
def Get_Result(str_xpath, tree, file):
    result = tree.xpath(str_xpath)
    print(result[0].strip())
    print(len(result))
    book = xlwt.Workbook('utf-8', style_compression=0)
    sheet = book.add_sheet("地点|概述", cell_overwrite_ok=True)
    sheet.write(0, 1, "地点")
    sheet.write(0, 2, "概述")
    j = 1
    for i in range(0, len(result)-1, 2):
        sheet.write(j, 1, result[i].strip())
        sheet.write(j, 2, result[i+1].strip())
        j += 1
    if os.path.exists(file):   # 如果本地系统中存在文件 file。
        os.remove(file)    # 删除本地文件 file。
    book.save(file)
    return result
#</editor-fold
#<editor-fold desc="***爬链接***"
def Get_Result_link(str_xpath, tree, file):
    result = tree.xpath(str_xpath)
    with open(file, "w" ,encoding='utf-8') as f:
        for (name, i) in zip(result, range(1, 100)):
                f.write(str(i)+": "+name+"\n")
    return result
#</editor-fold

# -----------得到首页页面-----------
url = r"http://bj.58.com/tech/pve_5363_245_pve_5358_0/" # https://movie.douban.com/
Home_file = r"E:\A爬虫文件\Xpath\page\A_page.txt"              # http://bj.58.com/tech/pve_5363_245_pve_5358_0/
tree = Get_page(url,Home_file)

# -----------爬公司名-------------
name_xpath = r'//*[@id="list_con"]/li/div[1]/div[1]/a/span/text()'
Name_file = r"E:\A爬虫文件\Xpath\name\A_name.xlsx"
Name = Get_Result(name_xpath, tree, Name_file)

# -----------爬链接---------------
link_xpath = r'//*[@id="list_con"]/li/div[1]/div[1]/a/@href'
link_file = r"E:\A爬虫文件\Xpath\link\A_link.txt"
link = Get_Result_link(link_xpath, tree, link_file)

# -----------爬所有连接的页面-------
ftree = "E:\A爬虫文件\AAA.txt"
for i in range(1, len(link)):
    file = str.format("E:\A爬虫文件\Xpath\page\B_page{0}.txt",i)
    try:
        tree = Get_page(link[i], file)
        print("已载入第 %d 个页面..." % i)
    except:
        print("未知错误！")

