#! -*- coding: utf-8 -*-
import json
import os
import re

import time
from scrapy import Request, FormRequest
from scrapy.spiders import CrawlSpider
from bs4 import BeautifulSoup
import requests
from Academician.items import IitbXxgkItem, IitbZwgkItem


class IitbSpider(CrawlSpider):
    """海南工业和信息化厅:::最新信息:::工作动态"""

    name = "IitbSpider"
    start_urls = ["http://iitb.hainan.gov.cn/zxgzdt/index_5.html", "http://iitb.hainan.gov.cn/zwgk/2/index_5.html", "http://iitb.hainan.gov.cn/zwgk/zcfg/index_5.html"]

    def parse(self, response):
        links = response.xpath("/html/body/div[1]/table/tr/td[2]/table/tr/td[2]/table[3]/tr/td[1]/a")
        if links == []:
            links = response.xpath("/html/body/div[1]/table/tr/td[2]/table/tr/td[1]/table[4]/tr/td[1]/a")
        for lin in links:
            url = lin.xpath("@href").extract()[0]
            title = lin.xpath("text()").extract()[0]
            data = {}
            data["title"] = title
            if "hainan.gov.cn" not in url:
                try:
                    try:
                        url = "http://iitb.hainan.gov.cn" + url.split("../..")[1]
                    except:
                        url = "http://iitb.hainan.gov.cn" + url.split("..")[1]
                except:
                     url = "http://iitb.hainan.gov.cn/zwgk/2/" + url.split("./")[1]
                finally:
                    pass
            data["url"] = url
            if "zwgk/" in url:
                """工作动态"""
                yield Request(url=url, callback=self.parse_zwgk, meta={"data": data})
            elif "xxgk." in url:
                """最新信息"""
                yield Request(url=url, callback=self.parse_xxgk, meta={"data": data})
            elif "tpxw/" in url:
                yield Request(url=url, callback=self.parse_zwgk, meta={"data": data})
            elif "tcsjtsdwlxdh" in url:
                yield Request(url=url, callback=self.parse_zwgk, meta={"data": data})



    def parse_xxgk(self, response):
        data = response.meta["data"]
        soup = BeautifulSoup(response.body, "lxml")
        msg = soup.find("table").find_all("table")[3].find_all("td", class_="a3D")
        indexNum = msg[0].get_text(strip=True).split(u"：")[1]
        topic = msg[1].find("span").get_text(strip=True)
        agency = msg[2].get_text(strip=True)
        group = msg[3].get_text(strip=True)
        DocumentNum = msg[6].get_text(strip=True)
        pushTime = msg[7].get_text(strip=True)
        topicWord = msg[8].get_text(strip=True)
        data["indexNum"] = indexNum
        data["topic"] = topic
        data["agency"] = agency
        data["group"] = group
        data["DocumentNum"] = DocumentNum
        data["pushTime"] = pushTime
        data["topicWord"] = topicWord
        try:
            TRS_PreAppend = soup.find("div", class_="TRS_PreAppend")
            content = TRS_PreAppend.get_text(strip=True)
        except:
            TRS_PreAppend = soup.find("font", {"id":"Zoom"})
            content = TRS_PreAppend.get_text(strip=True)
        imgList = TRS_PreAppend.find_all("img")
        data["content"] = content
        data["imgMsg"] = []
        for img in imgList:
            imgMsg = {}
            imgName = img["src"].split("./")[1]
            imgMsg['imgName'] = imgName
            imgUrl = data["url"].split("t2017")[0] + imgName
            imgMsg['imgUrl'] = imgUrl
            file_path = "data/" + self.name + "/" + indexNum.replace("/", "-") + "/"
            if not os.path.exists(file_path):
                os.makedirs(file_path)
            imgPath = file_path + imgName
            sess = requests.Session()
            try:
                try:
                    file_data = sess.get(imgUrl, timeout=10).content
                except:
                    file_data = sess.get(imgUrl, timeout=10).content
                with open(imgPath, "wb") as fd:
                    fd.write(file_data)
            except:
                pass
            imgMsg["imgPath"] = imgPath
            data["imgMsg"].append(imgMsg)
        fileList = soup.find("font", {"id": "Zoom"}).find_all("a")
        data["fileMsg"] = []
        for file in fileList:
            fileMsg = {}
            try:
                fileName = file["href"].split("./")[1]
                fileUrl = data["url"].split("t2017")[0] + fileName
            except:
                fileUrl = file["href"]
                fileName = fileUrl.split("/part/")[1]
            fileMsg['fileName'] = fileName
            fileMsg['fileUrl'] = fileUrl
            file_path = "data/" + self.name + "/" + indexNum.replace("/", "-") + "/"
            if not os.path.exists(file_path):
                os.makedirs(file_path)
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
        item = IitbXxgkItem()
        for key, val in data.items():
            item[key] = val
        yield item


    def parse_zwgk(self, response):
        data = response.meta["data"]
        try:
            keyword = response.xpath("/html/body/div[1]/table/tr/td[2]/table/tr/td/table/tr/td/table[1]/tr[2]/td/a[3]")
        except:
            keyword = response.xpath("/html/body/div[1]/table/tr/td[2]/table/tr/td/table/tr/td/table[1]/tr[2]/td/a[2]")
        data["keyword"] = keyword.xpath("text()").extract()[0]
        soup = BeautifulSoup(response.body, "lxml")
        ed = soup.find("div", {"class": "TRS_Editor"})
        content = ed.get_text(strip=True)
        data["content"] = content
        imgList = ed.find_all("img")
        data["imgMsg"] = []
        for img in imgList:
            imgMsg = {}
            imgName = img["src"].split("./")[1]
            imgUrl = data["url"].split("t2017")[0] + imgName
            file_path = "data/" + self.name + "/" + data["keyword"] + "/"
            if not os.path.exists(file_path):
                os.makedirs(file_path)
            imgMsg["imgName"] = imgName
            imgPath = file_path + imgName
            sess = requests.Session()
            try:
                try:
                    file_data = sess.get(imgUrl, timeout=10).content
                except:
                    file_data = sess.get(imgUrl, timeout=10).content
                with open(imgPath, "wb") as fd:
                    fd.write(file_data)
            except:
                pass
            imgMsg["imgPath"] = imgPath
            data["imgMsg"].append(imgMsg)
        try:
            fileList = soup.find("font", {"id": "Zoom"}).find_all("a")
        except:
            fileList = soup.find("td", {"id": "Zoom"}).find_all("a")
        data["fileMsg"] = []
        for file in fileList:
            fileMsg = {}
            fileName = file["href"].split("./")[1]
            fileMsg['fileName'] = fileName
            fileUrl = data["url"].split("t2017")[0] + fileName
            fileMsg['fileUrl'] = fileUrl
            file_path = "data/" + self.name + "/" + data["keyword"] + "/"
            if not os.path.exists(file_path):
                os.makedirs(file_path)
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
        item = IitbZwgkItem()
        for key, val in data.items():
            item[key] = val
        yield item





