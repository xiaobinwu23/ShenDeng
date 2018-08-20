#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 得到岗位，然后根据岗位得到技能点。
from multiprocessing.pool import ThreadPool
from lxml import html
import requests
import xlwt
import re
import jieba.posseg as pseg
import datetime

class Get_SPofPost:
    # ----------初始化------------
    def __init__(self):
        self.results = []
        self.count = 0
        self.gwName = ""
        self.book = xlwt.Workbook('utf-8')
        self.sheet = self.book.add_sheet("岗位—技能点")
        self.mstring = ""
    # ----------得到岗位----------
    def get_post(self, url):
        page = requests.get(url)
        tree = html.fromstring(page.text)
        result_name = tree.xpath(r'//*[@id="filterJob"]/ul/li/a/text()')   # 岗位名称
        result_href = tree.xpath(r'//*[@id="filterJob"]/ul/li/a/@href')   # 岗位链接
        result_name = result_name[1:50]   # 去掉第一个
        result_href = result_href[1:50]
        k = 0
        for (n, h) in zip(result_name, result_href):  # 遍历岗位
            if re.split('/', h)[0] != "http:":
                continue
            # 初始化
            self.mstring = ""
            self.results = []
            start = datetime.datetime.now()
            # 得到招聘链接 并 得到岗位需求
            self.get_recruit(h)
            # 通过岗位需求得到分词后的技能点
            self.MessageTojieba(self.mstring)
            # 把得到的岗位技能点写入Excel表
            self.sheet.write(k, 0, n)
            k += 1
            dic = {}
            for r in set(self.results):   # 转为dict类型
                dic[r] = self.results.count(r)
            dic_list = sorted(dic.items(), key=lambda item: item[1], reverse=True)   # 根据value排序（降序）
            for dl in dic_list:
                self.sheet.write(k, 1, dl[0])
                self.sheet.write(k, 2, dl[1])
                k += 1
            end = datetime.datetime.now()
            print(n+"岗位  已爬完！  用时：" + str(end - start))
        self.sheet.write(k, 0, "爬取的总岗位数：")
        self.sheet.write(k, 1, self.count)
        self.book.save(r"E:\1AAA\岗位-技能点\58同城-上海-技能点爬取.xls")
    # ----------得到招聘链接-------
    def get_recruit(self, url):
        page = requests.get(url)
        tree = html.fromstring(page.text)
        result_pages = tree.xpath(r'//*[@class="total_page"]/text()')   # 得到总页数
        pageCount = int(result_pages[1]) + 1
        gw = re.split('/', url)[3]   # 得到岗位英文
        for i in range(1, pageCount):   # 遍历页
            url2 = str.format("http://sh.58.com/{0}/pn{1}/?key=%E8%AE%A1%E7%AE%97%E6%9C%BA&final=1&jump=1&PGTID=0d302f82-0000-296d-cdf2-3edb04285a4c&ClickID=3", gw, i)
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
    # 计算机专业
    url = r"http://sh.58.com/tech/?PGTID=0d302408-0000-2991-9ceb-e40a6842f205&ClickID=1"
    obj = Get_SPofPost()
    obj.get_post(url)
