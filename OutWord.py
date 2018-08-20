#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 尝试爬取百度文档
from lxml import html
from selenium import webdriver
import re
from docx import Document

# 导一页文档
def GetPage():
    # 模拟运行
    driver = webdriver.Chrome('D:\Google\Chrome\Application\chromedriver.exe')
    driver.get('https://wenku.baidu.com/view/f3b460ab951ea76e58fafab069dc5022aaea46f1.html')
    # 获取页面
    page = driver.page_source
    tree = html.fromstring(page)
    # 筛选内容
    result = tree.xpath(r'//*[@id="pageNo-1"]/div/div/div/div/div/p/text()')
    # 筛选标题
    title = tree .xpath(r'/html/head/title/text()')
    # 获取内容位置
    style = tree.xpath(r'//*[@id="pageNo-1"]/div/div/div/div/div/p/@style')
    wieth = []
    for s in style:
        pattern = re.compile(r'.*top:(.*?)px.*')
        top = re.findall(pattern, s)
        wieth.append(top[0])
    # 排版
    last = 0
    ans = ""
    for (a, b) in zip(result, wieth):
        if a[len(a)-1] == '\n':
            a = a[:-1]
        if b != last:
            ans = ans + "\n" + a
        else:
            ans = ans + a
        last = b
    page = driver.find_elements_by_xpath("//div[@class='page']")
    driver.execute_script('arguments[0].scrollIntoView();', page[-1])  # 拖动到可见的元素去
    # sa = driver.find_element_by_xpath(r'//*[@id="wk_container"]/a')
    # sa.click()
    # driver.close()
    return title[0], ans

(title, ans) = GetPage()
doc = Document()
p = doc.add_paragraph(ans)
save_path = str.format(r"E:\1AAA\{0}.docx", title)
doc.save(save_path)