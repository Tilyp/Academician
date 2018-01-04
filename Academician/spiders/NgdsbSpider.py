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

from Academician.items import NgdsbItem


class NgdsbSpider(CrawlSpider):
    name = "NgdsbSpider"
    """海南都市报"""
    current_time = time.strftime('%Y-%m--%d', time.localtime(time.time()))  # 当前时间
    base_url = "http://ngdsb.hinews.cn/html/%s/%s/node_2.htm"
    host = "http://ngdsb.hinews.cn"

    def start_requests(self):
        date_str = self.current_time.split("--")
        req_url = self.base_url % (date_str[0], date_str[1])
        yield Request(url=req_url, callback=self.parse)

    def parse(self, response):
        soup = BeautifulSoup(response.body, "lxml")
        i = True
        ind = 1
        while i:
            try:
                StrId = "content_2_%s" % str(ind)
                tad = soup.find("div", {"id": StrId}).find("a")
                link = tad["href"]
                title = tad.get_text(strip=True)
                text_url = response.url.split("node")[0]
                req_url = text_url + link
                # req_url = "http://ngdsb.hinews.cn/html/2017-12/25/content_2_2.htm"
                data = {"url": req_url, "title": title}
                ind += 1
                yield Request(url=req_url, callback=self.parse_text, meta={"data": data})
            except:
                i = False

    def parse_text(self, response):
        data = response.meta["data"]
        soup = BeautifulSoup(response.body, "lxml")
        content = soup.find("div", {"id": "ozoom"}).get_text(strip=True)
        dateTime = soup.find("span", class_="default").get_text(strip=True)
        # try:
        #     newspic = soup.find("a", {"class": "pirobox_gall"})
        #     desc = newspic["title"]
        #     img = newspic.find("img")["src"].replace("../../..")
        #     imgUrl = self.host + img
        #
        #     data["imgUrl"] = imgUrl
        #     data["desc"] = desc
        #     data["imgPath"] = "Null"
        # except:
        #     data["imgUrl"] = "Null"
        #     data["desc"] = "Null"
        #     data["imgPath"] = "Null"

        data["dataTime"] = dateTime
        data["content"] = content
        item = NgdsbItem()
        for key, val in data.items():
            item[key] = val
        yield item