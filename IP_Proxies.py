#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 获取代理ip
import requests
from selenium import webdriver
from lxml import html

# 获取当前请求的IP地址
# page = requests.get("http://icanhazip.com", headers=headers, proxies=pro)
# print(page.text)

class IP_List:
    def __init__(self):
        pass
    # 返回代理IP列表
    def Get_IP_List(self):
        url = r"http://www.xicidaili.com/nn/"
        # options = webdriver.ChromeOptions()
        # options.add_argument('user-agent="Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19"')
        driver = webdriver.Chrome('D:\Google\Chrome\Application\chromedriver.exe')
        driver.get(url)
        page = driver.page_source
        driver.close()

        tree = html.fromstring(page)
        IPs = tree.xpath(r'//*[@id="ip_list"]/tbody/tr/td[2]/text()')
        Ports = tree.xpath(r'//*[@id="ip_list"]/tbody/tr/td[3]/text()')
        Tran = tree.xpath(r'//*[@id="ip_list"]/tbody/tr/td[6]/text()')
        li = []
        for (i, p, t) in zip(IPs, Ports, Tran):
            if t == "HTTP":
                ip = str.format("http://{0}:{1}", i, p)
                li.append(ip)
        for i in li:
            try:
                prox = {"http": i}
                requests.get(url, prox)
            except:
                li.remove(i)
        return li
