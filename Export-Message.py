
# 得到具体英文能力

import requests
from lxml import html
from tkinter import *
import re
import xlwt

# ------------开始爬---爬取招聘信息
def Get_Message(url):
   # url = "http://sh.58.com/job/pn3/?key=计算机专业软件开发&final=1&jump=1&PGTID=0d302408-0000-23eb-da8e-f8db44cac965&ClickID=3"
   page = requests.get(url)
   tree = html.fromstring(page.text)
   ans = tree.xpath('//*[@class="job_item clearfix"]/div[1]/div/a/@href')  # 得到所有招聘链接
   global gwSum
   # 遍历招聘链接
   for tj in ans:
     if "http://gz" not in tj:  # 过滤链接
       continue
     gwSum +=1   # 统计爬取的招聘信息个数
     pageC = requests.get(tj)

     treeC = html.fromstring(pageC.text)
     ansC = treeC.xpath('//*[@class="des"]/br')   # 得到 任职要求一栏的信息
     # 遍历内容
     i = 0
     for b in ansC:   # 确定 任职要求一栏
       bt = b.tail
       list_gw = ['岗位职责','岗位要求', '任职要求', '职位要求', '招聘要求', '任职资格']
       if bt[0]>'9' or bt[0]<'0':
         i=0
       if i == 1:
          list_nl = ['熟悉', '熟练', '掌握', '经验', '能力']   # 关键字过滤
          bt = bt[2:]
          for li in list_nl:   # 对 任职要求 过滤
            if li in bt:
              pattern = r"[A-Za-z]"     # 英文过滤 选择包含英文的
              ans = re.search(pattern, bt)
              if bool(ans):
                s = ""
                for w in bt:
                    if w < u'\u4e00' or w > u'\u9fa5':  # 中文过滤，去掉中文
                        s += w
                ans = re.split("[,/、+，]", s)  # 拆分
                for i in ans:
                    result = re.sub("[);；。！-]", "", i)  # 其他字符过滤
                    if len(result) == 0:
                        continue
                    result = result.strip()
                    for j in range(len(result)):   # 去除首字母的数字
                       if result[0]>='0' and result[0]<='9':
                           result = result[1:]
                       else :
                           break
                    if len(result.strip()) == 0:
                        continue
                    tj = result.strip().lower()  # 去除首尾空格，并把它全改为小写。
                    # 统计
                    if tj in se:
                        dic[tj] += 1
                    else:
                        dic[tj] = 1
                        se.add(tj)
       for lis in list_gw:   # 任职要求 开始
         if lis in bt:
           i=1


# -----------开始爬虫---确定爬虫的网址---
def get_f():
  root.destroy()  # 关闭窗体
  space = var.get()
  major = var2.get()
  for i in range(1, 6):
    url = str.format("http://{0}.58.com/job/pn{1}/?key={2}&final=1&jump=1&PGTID=0d302408-0000-23eb-da8e-f8db44cac965&ClickID=3", space, i, major)
    Get_Message(url)   # ------进一步爬虫---

  book = xlwt.Workbook(encoding='utf-8')   # 写入Excel表。
  sheet = book.add_sheet("58同城")
  k = 1

  for i in dic:  # 输出统计结果
      sheet.write(k, 0, i)
      sheet.write(k, 1, int(dic[i]))
      k += 1
  sheet.write(k+1, 0, "爬取的总岗位数")
  sheet.write(k+1, 1, gwSum)
  book.save(r"E:\1AAA\58同城-广州-计算机软件开发-能力需求.xls")

# --------------------------开始---------------------------#

# --------全局属性----------
gwSum = 0   # 总岗位数
dic = {}  # 统计
se = set()
# -------tkinter--可视化-----------
root = Tk()
root.title("58同城信息爬取")
root.geometry('500x500')

lab = Label(root, text="城市首字母", font=("宋体", 12), width=14, height=1).pack()
lab2 = Label(root, text="岗位", font=("宋体", 12), width=14, height=1).pack()

var = StringVar()
entry = Entry(root, textvariable=var)
entry.pack()
var2 = StringVar()
entry2 = Entry(root, textvariable=var2)
entry2.pack()
# ------------触发事件---开始爬虫-----
button = Button(root, text="爬取", command=get_f).pack()
root.mainloop()








