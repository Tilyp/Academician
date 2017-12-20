#! -*- coding: utf-8 -*-
import os

from scrapy import Request
from scrapy.spiders import CrawlSpider
from bs4 import BeautifulSoup
import requests

from Academician.items import CasadItem


class CasadSpider(CrawlSpider):

    name = "CasadSpider"

    start_urls = ["http://www.casad.cas.cn/chnl/372/index.html", "http://www.casad.cas.cn/chnl/373/index.html",
                  "http://www.casad.cas.cn/chnl/374/index.html", "http://www.casad.cas.cn/chnl/375/index.html",
                  "http://www.casad.cas.cn/chnl/376/index.html", "http://www.casad.cas.cn/chnl/377/index.html"
                  ]

    def parse(self, response):
        soup = BeautifulSoup(response.body, "lxml")
        spans = soup.find("dl", {"id": "allNameBar"}).find_all("span")
        for span in spans[1:]:
            url = span.find("a")["href"]
            yield Request(url=url, callback=self.parse_detail, dont_filter=True)
            # break
    def parse_detail(self, response):
        soup = BeautifulSoup(response.body, "lxml")
        div = soup.find("div", class_="contentTest")
        resume = div.get_text(strip=True)
        acadImg = div.find("div", class_="acadImg").find("img")
        imgUrl = acadImg["src"]
        file_data = requests.get(imgUrl).content
        name = acadImg["alt"]
        identity = soup.find("div", class_="currBar").find_all("a")[-1].get_text(strip=True)
        file_path = "data/" + self.name + "/" + identity + "/"
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        imgPath = file_path + name + ".png"
        with open(imgPath, "wb") as fd:
            fd.write(file_data)
        item = CasadItem()
        item["name"] = name
        item["identity"] = identity
        item["resume"] = resume
        item["url"] = response.url
        item["imgPath"] = imgPath
        item["imgUrl"] = imgUrl
        yield item

