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
from Academician.items import CkcestItem, HkwbItem


class HkwbSpider(CrawlSpider):
    name = "HkwbSpider"
    """海口日报"""
    current_time = time.strftime('%Y-%m--%d', time.localtime(time.time()))  # 当前时间
    base_url = "http://szb.hkwb.net/szb/html/%s/%s/node_2.htm"

    def start_requests(self):
        date_str = self.current_time.split("--")
        req_url = self.base_url % (date_str[0], date_str[1])
        yield Request(url=req_url, callback=self.parse)

    def parse(self, response):
        soup = BeautifulSoup(response.body, "lxml")
        tab = soup.find("table").find_all("table")
        links = tab[17].find_all("td")[1].find("table").find_all("a")
        for li in links:
            link = li["href"]
            title = li.get_text(strip=True)
            text_url = response.url.split("node")[0]
            req_url = text_url + link
            # req_url = "http://szb.hkwb.net/szb/html/2017-12/25/content_269867.htm"
            data = {"title": title, "url": req_url}
            yield Request(url=req_url, callback=self.parse_text, meta={"data": data})

    def parse_text(self, response):
        soup = BeautifulSoup(response.body, "lxml")
        content = soup.find("div", {"id": "ozoom"}).get_text(strip=True)
        dateTime = soup.find("span", class_="default").get_text(strip=True)
        data = response.meta["data"]
        data["dataTime"] = dateTime
        data["content"] = content
        item = HkwbItem()
        for key, val in data.items():
            item[key] = val
        yield item

