#! -*- coding: utf-8 -*-
import json
import os
import random
import re

import time
from scrapy import Request, FormRequest
from scrapy.spiders import CrawlSpider
from bs4 import BeautifulSoup
import requests
from Academician.items import KgxjItem
from Academician.user_agents import agents


class KgxjSpider(CrawlSpider):
    """海口科工信局:::工作动态:::政策法规:::行业动态"""

    name = "KgxjSpider"
    host = "http://kgxj.haikou.gov.cn"
    base_url = "http://kgxj.haikou.gov.cn/index.php?m=content&c=index&a=lists&catid=%s&page=%s"

    def start_requests(self):
        cids = [36, 59, 62]
        for cid in cids:
            req_url = self.base_url % (cid, 1)
            data = {"cid": cid, "page": 1}
            yield Request(url=req_url, callback=self.parse, meta={"data": data})

    def parse(self, response):
        soup = BeautifulSoup(response.body, "lxml")
        data = response.meta["data"]
        links = soup.find("div", class_="tzbox").find_all("a")
        for link in links:
            title = link.get_text(strip=True)
            url = link["href"]
            req_url = self.host + url
            detail = {}
            detail["url"] = req_url
            detail["title"] = title
            yield Request(url=req_url, callback=self.parse_detail, meta={"data": detail})
        paging = soup.find("div", class_="paging clearfix ").find("a").get_text()
        totalpage = re.findall("\d+", paging)[0]
        if int(totalpage) > data["page"]:
            data["page"] += 1
            next_url = self.base_url % (data["cid"], data["page"])
            yield Request(url=next_url, callback=self.parse, meta={"data": data})

    def parse_detail(self, response):
        soup = BeautifulSoup(response.body, "lxml")
        data = response.meta["data"]
        keyword = soup.find("h3", class_="fl").get_text(strip=True)
        data['keyword'] = keyword
        notice_text = soup.find("div", class_="notice-text")
        content = notice_text.get_text(strip=True)
        detail = notice_text.find("p", class_="sub-author").find_all("span")
        pushTime = detail[0].get_text(strip=True)
        author = detail[1].get_text(strip=True)
        source = detail[2].get_text(strip=True)
        data['pushTime'] = pushTime
        data['author'] = author
        data['source'] = source
        data['content'] = content
        imgList = notice_text.find_all("img")
        data['imgMsg'] = []
        for img in imgList:
            imgMsg = {}
            imgUrl = self.host + img["src"]
            try:
                imgName = img["alt"]
            except:
                imgName = imgUrl.split("/")[-1]

            imgMsg["imgName"] = imgName
            imgMsg["imgUrl"] = imgUrl
            file_path = "data/" + self.name + "/" + data["keyword"] + "/"
            if not os.path.exists(file_path):
                os.makedirs(file_path)
            filePath = file_path + imgName
            imgMsg["imgPath"] = filePath
            sess = requests.Session()
            headers = {}
            headers["User-Agent"] = random.choice(agents)
            try:
                try:
                    file_data = sess.get(imgUrl, timeout=10, headers=headers).content
                except:
                    file_data = sess.get(imgUrl, timeout=10, headers=headers).content
                with open(filePath, "wb") as fd:
                    fd.write(file_data)
            except:
                pass
            data["imgMsg"].append(imgMsg)
        item = KgxjItem()
        for key, val in data.items():
            item[key] = val
            # print key
        yield item



