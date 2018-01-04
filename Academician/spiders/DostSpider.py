#! -*- coding: utf-8 -*-
import json
import os
import re

import time
from scrapy import Request, FormRequest
from scrapy.spiders import CrawlSpider
from scrapy import Selector
from bs4 import BeautifulSoup
import requests
from Academician.items import DostItem, DostOthItem


class DostSpider(CrawlSpider):
    name = "DostSpider"
    """海南省科技厅::::政策解读::::工作动态::::媒体聚焦::::通知公告"""
    host = "http://dost.hainan.gov.cn"
    # start_urls = ["http://dost.hainan.gov.cn/col/col454/index.html"]

    def start_requests(self):
        start_urls = ["http://dost.hainan.gov.cn/col/col454/index.html", "http://dost.hainan.gov.cn/col/col415/index.html",
                      "http://dost.hainan.gov.cn/col/col416/index.html", "http://dost.hainan.gov.cn/col/col417/index.html"]
        keyword = [u"政策解读", u"工作动态", u"媒体聚焦", u"通知公告"]
        for ind, url in enumerate(start_urls):
            req_url = url
            key = keyword[ind]
            data = {"keyword": key}
            yield Request(url=req_url, callback=self.parse, meta={"data": data})

    def parse(self, response):
        soup =BeautifulSoup(response.body, "lxml")
        data = response.meta["data"]
        if data["keyword"] == u"政策解读":
            text = soup.find("div", {"id": "282"}).get_text(strip=True).split("href='")
            for te in text[1:-1]:
                req_url = self.host + te.split("' class='bt_link'")[0]
                data["url"] = req_url
                yield Request(url=req_url, callback=self.parse_con, meta={"data": data})
        elif data["keyword"] == u"通知公告":
            text = soup.find("div", {"id": "123"}).get_text(strip=True).split("href='")
            for te in text[1:-1]:
                req_url = te.split("' class='bt_link'")[0]
                if self.host not in req_url:
                    req_url = self.host + req_url
                data["url"] = req_url
                yield Request(url=req_url, callback=self.parse_con, meta={"data": data})
        else:
            text = soup.find("div", {"id": "123"}).get_text(strip=True).split("href='")
            for te in text[1:-1]:
                req_url = self.host + te.split("' class='bt_link'")[0]
                data["url"] = req_url
                yield Request(url=req_url, callback=self.parse_oth, meta={"data": data})

    def parse_oth(self, response):
        data = response.meta["data"]
        soup = BeautifulSoup(response.body, "lxml")
        xwlb = soup.find("div", class_="xwlb").find("table").find_all("tr")
        title = xwlb[1].find("td").get_text(strip=True)
        data["title"] = title
        pushTime = xwlb[3].find("li", class_="fbrq").get_text(strip=True)
        infoSource = xwlb[3].find_all("li")[-1].get_text(strip=True)
        data["pushTime"] = pushTime
        data["infoSource"] = infoSource
        str_con = xwlb[4].find("div", {"id": "zoom"})
        content = str_con.get_text(strip=True)
        data["content"] = content
        imglinks = str_con.find_all("a")
        data["fileMsg"] = []
        if len(imglinks):
            for s in imglinks:
                fileMsg = {}
                fileUrl = self.host + s["href"]
                fileMsg["fileUrl"] = fileUrl
                file_path = "data/" + self.name + "/" + data["keyword"] + "/"
                if not os.path.exists(file_path):
                    os.makedirs(file_path)
                fileName = fileUrl.split("/0/")[1]
                fileMsg["fileName"] = fileName
                filePath = file_path + fileName
                sess = requests.Session()
                try:
                    try:
                        file_data = sess.get(fileUrl, timeout=10).content
                    except:
                        file_data = sess.get(fileUrl, timeout=10).content
                    with open(filePath, "wb") as fd:
                        fd.write(file_data)
                except:
                    pass
                fileMsg["filePath"] = filePath
                data["fileMsg"].append(fileMsg)
        item = DostOthItem()
        for key, val in data.items():
            item[key] = val
        yield item





    def parse_con(self, response):
        soup = BeautifulSoup(response.body, "lxml")
        xwlb = soup.find("div", class_="xwlb").find("table").find_all("tr")
        str_t = xwlb[0].find_all("td")
        data = response.meta["data"]
        indexNum = str_t[1].get_text(strip=True)
        data["url"] = response.url
        data["indexNum"] = indexNum
        openTime = str_t[3].get_text(strip=True)
        data["openTime"] = openTime
        str_e = xwlb[1].find_all("td")
        Publisher = str_e[1].get_text(strip=True)
        data["Publisher"] = Publisher
        DocumentNum = str_e[3].get_text(strip=True)
        data["DocumentNum"] = DocumentNum
        xwlbs = soup.find("div", class_="xwlb").find_all("table")[1].find_all("tr")
        title = xwlbs[1].find("td").get_text(strip=True)
        data["title"] = title
        pushTime = xwlbs[3].find("li", class_="fbrq").get_text(strip=True)
        data["pushTime"] = pushTime
        str_con = xwlbs[4].find("div", {"id": "zoom"})
        content = str_con.get_text(strip=True)
        data["content"] = content
        files = str_con.find_all("a")
        data["fileMsg"] = []
        if len(files):
            for s in files:
                fileMsg = {}
                fileUrl = self.host + s["href"]
                fileMsg["fileUrl"] = fileUrl
                file_path = "data/" + self.name + "/" + indexNum.replace("/", "-") + "/"
                if not os.path.exists(file_path):
                    os.makedirs(file_path)
                fileName = s.get_text(strip=True)
                fileMsg["fileName"] = fileName
                filePath = file_path + fileName
                sess = requests.Session()
                try:
                    try:
                        file_data = sess.get(fileUrl, timeout=10).content
                    except:
                        file_data = sess.get(fileUrl, timeout=10).content
                    with open(filePath, "wb") as fd:
                        fd.write(file_data)
                except:
                    pass
                fileMsg["filePath"] = filePath
                data["fileMsg"].append(fileMsg)
        item = DostItem()
        for key, val in data.items():
            item[key] = val
        yield item


