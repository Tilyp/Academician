#! -*- coding: utf-8 -*-
import json
import os
import random
import re
from scrapy import Request, FormRequest
from scrapy.spiders import CrawlSpider
from bs4 import BeautifulSoup
import requests
from Academician.items import HnPeopleItem


class HnPeopleSpider(CrawlSpider):
    """海南人民政府:::十二大产业"""
    name = "HnPeopleSpider"
    host = "http://www.hainan.gov.cn/"

    start_urls = ["http://www.hainan.gov.cn/hn/zt/jsfzl/zdcy/"]

    def parse(self, response):
        soup = BeautifulSoup(response.body, "lxml")
        leaidx = soup.find("div", class_="ej_zdcysto").find_all("h2")
        url = response.url
        url_list = ["http://www.hainan.gov.cn/hn/yw/jrhn/", "http://www.hainan.gov.cn/hn/yw/ldhd/", "http://www.hainan.gov.cn/hn/yw/zwdt/tj/"]
        for le in leaidx:
            flag = le.find("a")["href"].split("./")[1]
            text_url = url + flag
            url_list.append(text_url)
        for req_url in url_list:
            data = {"url": req_url}
            # req_url = "http://www.hainan.gov.cn/hn/zt/jsfzl/zdcy/rdtsgxnyhncfz/index_9.html"
            yield Request(url=req_url, callback=self.parse_detail, meta={"data": data})
            # break


    def parse_detail(self, response):
        data = response.meta["data"]
        soup = BeautifulSoup(response.body, "lxml")
        keyword = soup.find("div", class_="flfg_01").get_text(strip=True)
        url = data['url']
        flfg_02 = soup.find("div", class_="flfg_02").find_all("li")
        for li in flfg_02:
            links = li.find("a")
            try:
                req_url = url + links["href"].split("./")[1]
            except:
                req_url = links["href"]
            title = links.get_text(strip=True)
            detail = {}
            detail["keyword"] = keyword
            detail["baseUrl"] = data["url"]
            detail["url"] = req_url
            detail["title"] = title
            # req_url = "http://www.hainan.gov.cn/data/news/2017/12/180578/"
            yield Request(url=req_url, callback=self.parse_text, meta={"data": detail})
            # break
        try:
            page_bar = soup.find("div", {"class": "page_display"}).find_all("script")[1].get_text(strip=True)
            num = re.findall("\d+", page_bar)
            if int(num[1]) > int(num[2]):
                next_url = url + "index_%s.html" % str(int(num[2]) + 1)
                yield Request(url=next_url, callback=self.parse_detail, meta={"data": data})
        except Exception, e:
            print e
            pass

    def parse_text(self, response):
        data = response.meta["data"]
        soup = BeautifulSoup(response.body, "lxml")
        cy_ytbt = soup.find("div", class_="cy_ytbt").find_all("li")
        pushTime = cy_ytbt[1].get_text(strip=True)
        data["pushTime"] = pushTime
        editor = cy_ytbt[3].get_text(strip=True).split(u"【")[0]
        if len(editor) > 150:
            editor = cy_ytbt[2].get_text(strip=True)
        data["editor"] = editor
        strCon = soup.find("div", class_="TRS_Editor")
        if strCon == None:
            strCon = soup.find("div", {"id": "Zoom"})
        content = ""
        for con in strCon.find_all("p"):
            content += con.get_text(strip=True)
        data["content"] = content
        imgList = strCon.find_all("img")
        data['imgMsg'] = []
        for img in imgList:
            imgMsg = {}
            try:
                imgName = img["src"].split("./")[1]
                imgUrl = data["baseUrl"] + "201712/" + imgName
            except:
                imgUrl = img["src"]
                imgName = imgUrl.split("/")[-1]
            imgMsg["imgName"] = imgName
            imgMsg["imgUrl"] = imgUrl
            file_path = "data/" + self.name + "/" + data["keyword"] + "/"
            if not os.path.exists(file_path):
                os.makedirs(file_path)
            filePath = file_path + imgName
            imgMsg["imgPath"] = filePath
            sess = requests.Session()
            try:
                try:
                    file_data = sess.get(imgUrl, timeout=10).content
                except:
                    file_data = sess.get(imgUrl, timeout=10).content
                with open(filePath, "wb") as fd:
                    fd.write(file_data)
            except:
                pass
            data["imgMsg"].append(imgMsg)

        item = HnPeopleItem()
        for key, val in data.items():
            item[key] = val
        yield item


