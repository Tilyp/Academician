#! -*- coding: utf-8 -*-
import os
import re
from scrapy import Request
from scrapy.spiders import CrawlSpider
from bs4 import BeautifulSoup
import requests
from Academician.items import HkPeopleItem


class HkPeopleSpider(CrawlSpider):
    """海口人民网:::每日头条:::海口要闻"""

    name = "HkPeopleSpider"
    host = "http://www.haikou.gov.cn/zfdt/"
    base_url = "http://www.haikou.gov.cn/zfdt/%s/index%s.html"

    def start_requests(self):
        flag = ["mrtt", "hkyw"]
        for f in flag:
            req_url = self.base_url % (f, "")
            data = {"flag": f, "page": 1}
            yield Request(url=req_url, callback=self.parse, meta={"data": data})

    def parse(self, response):
        data = response.meta["data"]
        soup = BeautifulSoup(response.body, "lxml")
        column_c = soup.find("div", class_="column-c")
        links = column_c.find("ul").find_all("a")
        for link in links:
            title = link.get_text(strip=True)
            url = link["href"]
            req_url = self.host + data["flag"] + "/" + url.split("./")[1]
            detail = {}
            detail["flag"] = data["flag"]
            detail["url"] = req_url
            detail["title"] = title
            yield Request(url=req_url, callback=self.parse_detail, meta={"data": detail})
        page = soup.find("div", class_="page").find("script").get_text()
        pageNo = re.findall("\d+", page)
        if int(pageNo[0]) > int(pageNo[1]):
            next_url = self.base_url % (data["flag"], "_" + str(int(pageNo[1]) + 1))
            yield Request(url=next_url, callback=self.parse, meta={"data": data})




    def parse_detail(self, response):
        data = response.meta["data"]
        soup = BeautifulSoup(response.body, "lxml")
        detail = soup.find("div", class_="maincon-i").get_text().split(u"　　")
        webName = detail[0]
        undateTime = detail[1].strip()
        source = detail[2].strip()
        author = detail[3]
        if data["flag"] == "mrtt":
            data["keyword"] = u"每日头条"
        elif data["flag"] == "hkyw":
            data["keyword"] = u"海口要闻"
        data['webName'] = webName
        data['undateTime'] = undateTime
        data['source'] = source
        data['author'] = author
        docum = soup.find("div", {"id": "zl_Articel"})
        content = docum.get_text(strip=True)
        data["content"] = content
        imgList = docum.find_all("img")
        data['imgMsg'] = []
        for img in imgList:
            imgMsg = {}
            imgUrl = self.host + "/" + data["flag"] + "/201712/" + img["src"].split("./")[1]
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

        item = HkPeopleItem()
        for key, val in data.items():
            item[key] = val
            # print key
        yield item

