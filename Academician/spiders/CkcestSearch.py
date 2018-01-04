#! -*- coding: utf-8 -*-
import json
import os
import random
import re
from scrapy import Request, FormRequest
from scrapy.spiders import CrawlSpider
from bs4 import BeautifulSoup
import requests
from Academician.items import HnPeopleItem, CkcestSearchItem


class CkxestSearch(CrawlSpider):
    name = "CkxestSearch"
    keyword = ["旅游", "农业", "互联网", "医疗", "金融",
               "会展", "现代物流", "油气", "医药", "低碳制造",
               "房地产", "高新技术教育文化体育"]

    url = "http://www.ckcest.cn/default/search/getContent?db=800033&uni=1&word=%s&count=10&start=%s&country=中国&province=上海&city=上海&dbname=工程院院士&sortby=1"

    def start_requests(self):
        for key in self.keyword:
            num = 0
            req_url = self.url % (key, num)
            data = {"num": num, "key": key}
            yield Request(url=req_url, callback=self.parse, meta={"data": data})
            # break

    def parse(self, response):
        soup = json.loads(response.body)
        data = response.meta["data"]
        if soup["carriertype"] == u"院士":
            for records in soup["records"]:
                detail = {}
                deta = records["meta"]
                detail['name'] = deta[1]
                detail['sex'] = deta[3]
                detail['Nation'] = deta[4]
                detail['Birthday'] = deta[6]
                detail['SelectedTime'] = deta[5]
                detail['Ancestral'] = deta[7]
                detail['Country'] = deta[8]
                detail['Party'] = deta[11]
                detail['resume'] = deta[12].replace("&nbsp;", "").strip()
                detail['subject'] = deta[14]
                detail['Department'] = deta[15]
                item = CkcestSearchItem()
                for key, val in detail.items():
                    item[key] = val
                yield item
            hit = soup["hit"]
            if data["num"] == 0:
                data["hit"] = hit
            data["num"] += 10
            if int(data["hit"]) > int(data["num"]):
                req_url = self.url % (data['key'], data["num"])
                yield Request(url=req_url, callback=self.parse, meta={"data": data})