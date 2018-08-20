#!/usr/bin/env python
# _*_ coding: utf-8 _*_

import urllib.request
import re
from lxml import html

# 通过 url 把获取的网页内容输出到 file 中。
# 并返回 str类型的 网页内容。
def Get_str_page(url, file):
    Pagefile = open(file, "w", encoding='utf-8')
    requests = urllib.request.Request(url)
    with urllib.request.urlopen(requests) as f:
        strpage = str(f.read(), encoding="utf-8")   # read()后的内容为bytes类型,需要把他转换为str类型。
        Pagefile.write(strpage)
    Pagefile.close()
    return strpage

# 通过 pattern 把目标 string 正则后输出到 str_file 中。
#并返回 list类型的 正则内容。
def Get_Re_file(str_pattern, string, str_file):
    pattern = re.compile(str_pattern, re.M)
    result = re.findall(pattern, string)
    file=open(str_file, "w", encoding='utf-8')
    for (name,i) in zip(result,range(1,100)):
        file.write(str(i)+": "+name+"\n")
    file.close()
    return result

# -----------------爬取主页内容-----------------
url = r"http://bj.58.com/tech/pve_5363_245_pve_5358_0/"
Home_file = r"E:\A爬虫文件\Re\page\A_page.txt"
strpage=Get_str_page(url, Home_file)

# -----------------正则筛选公司名---------------
N_str_pattern = r'.*<span class="name">(.*)</span>.*'
Name_file = r"E:\A爬虫文件\Re\name\A_name.txt"
Get_Re_file(N_str_pattern,strpage,Name_file)

# -----------------正则筛选公司网址--------------
W_str_pattern = r'.*<a href="(.*)" urlparams.*'
W_file=r'E:\A爬虫文件\Re\link\A_link.txt'
Get_Re_file(W_str_pattern,strpage,W_file)
 # //*[@id="list_con"]/li[1]/div[1]/div[1]/a
 # //*[@id="list_con"]/li[2]/div[1]/div[1]/a