#! -*- coding: utf-8 -*-
import json
import os
import re
from scrapy import Request, FormRequest
from scrapy.spiders import CrawlSpider
from bs4 import BeautifulSoup
import requests
from Academician.items import CkcestItem


class WsspSpider(CrawlSpider):
    name = "WsspSpider"

    host = "http://wssp.hainan.gov.cn"
    base_url = "http://wssp.hainan.gov.cn/wssp/hn/module/wssp/wssb/sbindex.do"

    def start_requests(self):
        data = {"acc_id": "", "bmmc": "", "ddid": "HZ2881f4424539dd0142453d7336002c",
                "deptId": "HZ2881f4424539dd0142453d7336002c", "sxlx": "", "sxname": "",
                "HZ_PAGE_NO": "1", "HZ_PAGE_SIZE": "10", "pageNum": ""}
        yield FormRequest(url=self.base_url, formdata=data, meta={"data": data}, callback=self.parse)

    def parse(self, response):
        soup = BeautifulSoup(response.body, "lxml")
        buttons = soup.find("ul", class_="fn-clear").find_all("h1")
        for but in buttons:
            link = but.find("a")["href"]
            req_url = self.host + link
            yield Request(url=req_url, callback=self.parse_hn, dont_filter=True)
            break
        page_wrap = soup.find("div", class_="page_wrap").find("div", class_="fn-right").find("strong").get_text(strip=True)
        data = response.meta["data"]
        if int(page_wrap) > int(data["HZ_PAGE_NO"]):
            data["HZ_PAGE_NO"] = str(int(data["HZ_PAGE_NO"]) + 1)
            # yield FormRequest(url=self.base_url, formdata=data, meta={"data": data}, callback=self.parse)

    def parse_hn(self, response):
        soup = BeautifulSoup(response.body, "lxml")
        temp_main = soup.find("div", class_="public_temp_main_1 fn-clear")
        lawGuide_mainTit = temp_main.find("div", class_="lawGuide_mainTit fn-clear").get_text().split("\r")
        print lawGuide_mainTit
        # item_name =
        lawGuide_mainLeft = temp_main.find("div", class_="lawGuide_mainLeft")
        lawGuide_mainLeft_tit = lawGuide_mainLeft.find("div", class_="lawGuide_mainLeft_tit").get_text()
        base_msg = lawGuide_mainLeft.find("ul", class_="fn-clear").find_all("span")
        for msg in base_msg:
            print msg


