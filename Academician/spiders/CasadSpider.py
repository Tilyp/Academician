#! -*- coding: utf-8 -*-
from scrapy import Request
from scrapy.spiders import CrawlSpider
from bs4 import BeautifulSoup

class CasadSpider(CrawlSpider):

    name = "CasadSpider"

    start_urls = ["http://www.casad.cas.cn/chnl/371/index.html"]

    def parse(self, response):
        soup = BeautifulSoup(response.body, "lxml")
        spans = soup.find("dl", {"id": "allNameBar"}).find_all("span")
        for span in spans[1:]:
            url = span.find("a")["href"]
            yield Request(url=url, callback=self.parse_detail, dont_filter=True)
            break

    def parse_detail(self, response):
        soup = BeautifulSoup(response.body, "lxml")
        print soup

