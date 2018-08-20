#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 根据地点和关键字得到技能点

from tkinter import *
from lxml import html
import re
import requests
from GetPinying import Get_first_letter
import datetime
import jieba.posseg as pseg
import xlwt
from multiprocessing.dummy import Pool as ThreadPool

class Get_SP:
   def __init__(self):
       # 待分词的字符串
       self.mstring = ""
       # 分词后的结果
       self.results = []
       # 爬取的总岗位数
       self.count = 0
   # -----------将最终结果写入Excel表中-------
   def WriteToExcel(self, results):
       book = xlwt.Workbook('utf-8')
       sheet = book.add_sheet("技能点爬取")
       k = 1
       for r in set(results):
           sheet.write(k, 0, r)
           sheet.write(k, 1, results.count(r))
           k += 1
       sheet.write(k, 0, "爬取的岗位总数")
       sheet.write(k, 1, self.count)
       path = str.format(r"E:\1AAA\58同城-{0}-{1}-技能点爬取.xls", self.city.get(), self.job.get())
       book.save(path)

   # -----------jieba分词-------------------
   def MessageTojieba(self, mstr):
       ans = pseg.lcut(mstr)
       for i in range(len(ans)):
           if ans[i].word in ['能力', '经验']:   # 后缀过滤
               sp = ""
               for j in range(i, i-6, -1):
                   if ans[j].flag == 'x' or ans[j].word in ['有', '和']:
                       break
                   else: sp = ans[j].word + sp
               if sp != "能力":
                  self.results.append(sp)
           if ans[i].word in ['具备', '精通', '熟练', '熟悉']:   # 前缀过滤
               sp2 = ""
               for j in range(i+1, i+6):
                   if ans[j].flag == 'x' or ans[j].word in ['有', '和']:
                       break
                   else: sp2 = sp2 + ans[j].word
               if len(sp2) != 0:
                  self.results.append(sp2 + "能力")
           if ans[i].word in ['良好', '较强', '强烈', '一定']:   # 前缀过滤
               sp3 = ""
               for j in range(i, i+6):
                   if ans[j].flag == 'x' or ans[j].word in ['有', '和']:
                       break
                   else: sp3 = sp3 + ans[j].word
               if len(sp3) != 0:
                  self.results.append(sp3)

   # ---------通过岗位url得到岗位描述----------
   def UrlToMessage(self, url):
       self.count += 1
       page = requests.get(url)
       tree = html.fromstring(page.text)
       Messages = tree.xpath(r'//*[@class="des"]/br')
       ls_gw = ['条件', '职责', '要求', '任职', '资格', '招聘']
       ok = 0
       for m in Messages:
           m = m.tail
           ls_key = ['能力', '具备', '熟悉', '掌握', '熟练', '经验', '了解', '精通']
           if ok == 1:
               if m[0] >='0' and m[0]<='9':
                   for k in ls_key:   # 关键字过滤
                       if k in m:
                           m = m[1:]
                           self.mstring += m
               else :break
           for gw in ls_gw:   # 关键字过滤
               if gw in m:
                   ok = 1
   # ---------通过页面爬取岗位链接-------------
   def PageToUrl(self, page):
       tree = html.fromstring(page.text)
       urls = tree.xpath(r'//*[@class="job_item clearfix"]/div[1]/div/a/@href')
       # 多线程并行爬取
       pool = ThreadPool(10)
       pool.map(self.UrlToMessage, urls)
       pool.close()
       pool.join()
       # for url in urls:
       #     self.UrlToMessage(url)
   # -------------开始爬虫------------
   def Start(self):
       self.sroot.destroy()
       print("爬取中...")
       py = Get_first_letter(self.city.get())
       cityp = py.getPinyin()
       if self.city.get() == "深圳":
           cityp = "sz"
       jobp = self.job.get()
       for i in range(1, 70):
          s = datetime.datetime.now()
          url = str.format("http://{0}.58.com/job/pn{1}/?key={2}&final=1&jump=1&PGTID=0d302408-0000-23eb-da8e-f8db44cac965&ClickID=3", cityp, i, jobp)
          page = requests.get(url)
          self.PageToUrl(page)
          e = datetime.datetime.now()
          print("第 %d 页已爬完！  用时：%s"% (i, str(e - s)))
   # --------------可视化--------------
   def Visual(self):
       # ------主窗体-------
       root = Tk()
       self.sroot = root
       root.title("58同城信息爬取")
       root.geometry('500x500')
       # ------城市输入------
       lab = Label(root, text="城市名称", font=("宋体", 12), width=14, height=1).pack()
       self.city = StringVar()
       entry = Entry(root, textvariable=self.city)
       entry.pack()
       # ------岗位输入------
       lab2 = Label(root, text="岗位名称", font=("宋体", 12), width=14, height=1).pack()
       self.job = StringVar()
       entry2 = Entry(root, textvariable=self.job)
       entry2.pack()
       # ------------触发事件---开始爬虫-----
       button = Button(root, text="爬取", command=self.Start).pack()
       root.mainloop()

# -------------主函数--------------
if __name__ == '__main__':
    # 开始计时
    start = datetime.datetime.now()
    # 定义对象
    obj = Get_SP()
    # 可视化。点击按钮后开始爬取
    obj.Visual()
    # 把爬取的内容进行jieba分词
    obj.MessageTojieba(obj.mstring)
    # 把分词后的最终结果写入Excel表
    obj.WriteToExcel(obj.results)
    # 计时结束
    end = datetime.datetime.now()
    print(obj.mstring + "\n总用时：" + str(end - start))