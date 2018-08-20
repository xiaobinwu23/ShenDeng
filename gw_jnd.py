#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 根据岗位，得到多个城市的该岗位技能点
from multiprocessing.pool import ThreadPool
from lxml import html
import requests
import xlwt
import re
import jieba.posseg as pseg
import datetime
import random
from IP_Proxies import IP_List

class Get_SPofPost:
    # ----------初始化------------
    def __init__(self):
        self.results = []  # 最终结果（清洗后）
        self.count = 0     # 爬取的招聘信息总数
        self.gwName = "软件工程师"  # 岗位名
        self.mstring = ""   # 待清洗的数据
        self.ip_list = []   # 代理ip !!!还有问题
        # 请求头
        self.header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"}
    # ----------得到招聘链接-------
    def get_recruit(self, url):
        page = requests.get(url)
        tree = html.fromstring(page.text)
        result_pages = tree.xpath(r'//*[@class="total_page"]/text()')   # 得到总页数
        pageCount = int(result_pages[1]) + 1
        print("页数："+str(pageCount))
        ct = re.split('[/.]', url)[2]   # 得到城市英文
        for i in range(1, pageCount):   # 遍历页
            url2 = str.format("http://{0}.58.com/job/pn{1}/?key={2}&final=1&jump=1&PGTID=0d302408-0000-2a26-061e-060723970e49&ClickID=1", ct, i, self.gwName)
            try:
               page2 = requests.get(url2)
            except:
                print("访问网页出现异常！")
                continue

            tree2 = html.fromstring(page2.text)
            result_zp = tree2.xpath(r'//*[@class="job_item clearfix"]/div[1]/div/a/@href')
            for u in result_zp:
                if re.split('/', u)[0] != "http:":
                    result_zp.remove(u)
            pool = ThreadPool(10)
            pool.map(self.UrlToMessage, result_zp)
            pool.close()
            pool.join()
    # ----------得到岗位需求---------
    def UrlToMessage(self, url):
        self.count += 1
        print("当前岗位数："+str(self.count))
        page = requests.get(url)
        tree = html.fromstring(page.text)
        Messages = tree.xpath(r'//*[@class="des"]/br')
        ls_gw = ['条件', '职责', '要求', '任职', '资格', '招聘']
        ok = 0
        for m in Messages:
            m = m.tail
            ls_key = ['能力', '具备', '熟悉', '掌握', '熟练', '经验', '了解', '精通']
            if ok == 1:
                if m[0] >= '0' and m[0] <= '9':
                    for k in ls_key:  # 关键字过滤
                        if k in m:
                            m = m[1:]
                            self.mstring += m
                else:
                    break
            for gw in ls_gw:  # 关键字过滤
                if gw in m:
                    ok = 1
    # -----------得到技能点------------
    def MessageTojieba(self, mstr):
        ans = pseg.lcut(mstr)
        for i in range(len(ans)):
            if ans[i].word in ['能力', '经验']:  # 后缀过滤
                sp = ""
                for j in range(i, i - 6, -1):
                    if ans[j].flag == 'x' or ans[j].word in ['有', '和']:
                        break
                    else:
                        sp = ans[j].word + sp
                    if j <= 0:
                        break
                if sp != "能力":
                    self.results.append(sp)
            if ans[i].word in ['具备', '精通', '熟练', '熟悉']:  # 前缀过滤
                sp2 = ""
                for j in range(i + 1, i + 6):
                    if ans[j].flag == 'x' or ans[j].word in ['有', '和']:
                        break
                    else:
                        sp2 = sp2 + ans[j].word
                    if j+1 >= len(ans):
                        break
                if len(sp2) != 0:
                    self.results.append(sp2 + "能力")
            if ans[i].word in ['良好', '较强', '强烈', '一定']:  # 前缀过滤
                sp3 = ""
                for j in range(i, i + 6):

                    if ans[j].flag == 'x' or ans[j].word in ['有', '和', '.']:
                        break
                    else:
                        sp3 = sp3 + ans[j].word
                    if j+1 >= len(ans):
                        break
                if len(sp3) != 0:
                    self.results.append(sp3)
if __name__ == "__main__":

    obj = Get_SPofPost()
    citys = ['sh', 'sz', 'bj', 'gz', 'hz']# , 'cd', 'nj', 'tj', 'wh', 'cq'
    for c in citys:
        url = str.format(r"http://{0}.58.com/job/pn1/?key={1}&final=1&jump=1&PGTID=0d302408-0000-2a26-061e-060723970e49&ClickID=1", c, obj.gwName)
        start = datetime.datetime.now()
        print("开始咯："+url)
        obj.get_recruit(url)
        end = datetime.datetime.now()
        print(c + "城市已爬完！用时：" + str(end - start))
    obj.MessageTojieba(obj.mstring)
    # 写入Excel表
    book = xlwt.Workbook('utf-8')
    sheet = book.add_sheet("多个城市—"+obj.gwName)
    dic = {}
    k = 1
    for a in set(obj.results):
        dic[a] = obj.results.count(a)
    dic_list = sorted(dic.items(), key=lambda item: item[1], reverse=True)
    for dl in dic_list:
        sheet.write(k, 0, dl[0])
        sheet.write(k, 1, dl[1])
        k += 1
    sheet.write(k, 0, "爬取的总岗位数")
    sheet.write(k, 1, obj.count)
    path = str.format(r"E:\1AAA\岗位-技能点-多城市\58同城-{0}-技能点爬取.xls", obj.gwName)
    book.save(path) # 未经清洗的源数据
