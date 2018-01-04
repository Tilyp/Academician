#! -*- coding: utf-8 -*-
import json
import os
import random
import re
from scrapy import Request, FormRequest
from scrapy.spiders import CrawlSpider
from bs4 import BeautifulSoup
import requests
from Academician.items import ExpertItem
from Academician.user_agents import agents


class ExpertCkcest(CrawlSpider):
    name = "ExpertCkcest"
    host = "http://expert.ckcest.cn"
    keyword = [u"旅游", u"农业", u"互联网", u"医疗", u"金融",
               u"会展", u"现代物流", u"油气", u"医药", u"低碳",u"制造",
               u"房地产", u"高新技术",u"教育", u"文化", u"体育"]

    post_url = "http://expert.ckcest.cn/api/queryExperts"

    def start_requests(self):
        for key in self.keyword:
            data = {"name": "", "institute": "", "subject": "", "keyword": "房地产业", "from": "0", "size": "16"}
            data["keyword"] = key
            yield FormRequest(url=self.post_url, formdata=data, meta={"data": data},
                              callback=self.parse, dont_filter=True)

    def parse(self, response):
        soup = json.loads(response.body)
        data = response.meta["data"]
        for obj in soup["obj"]:
            # detail = {"nameOrgArray": str([obj])}
            # print detail
            # base_url = "http://expert.ckcest.cn/api/queryExpertSummary"
            # yield FormRequest(url=base_url, formdata=detail, meta={"data": detail},
            #                   callback=self.parse_summary, dont_filter=True)
            # break
            detail = {}
            detail['kId'] = obj["kId"]
            detail['name'] = obj["name"]
            detail['subject'] = obj["subject"]
            detail["level"] = data["keyword"]
            detail['keyword'] = obj["keyword"].strip()
            detail['organization'] = obj["organization"]
            req_url = "http://expert.ckcest.cn/detail?kid=%s" % detail['kId']
            yield Request(url=req_url, callback=self.parse_summary, meta={"data": detail, "PhantomJS": True})
            # break
        count = soup["count"]
        if int(data["from"]) <= int(count):
            data["from"] = str(int(data["from"]) + 16)
            yield FormRequest(url=self.post_url, formdata=data, meta={"data": data},
                              callback=self.parse, dont_filter=True)



    def parse_summary(self, response):
        data = response.meta["data"]
        soup = BeautifulSoup(response.body, "lxml")
        content = soup.find("div", class_="content ng-binding").get_text(strip=True)
        data['content'] = content
        try:
            img = soup.find("img", class_="avatar-img")["src"].split("..")[1]
        except:
            img = soup.find("img", class_="avatar-img")["src"]
        imgUrl = self.host + img
        file_path = "data/" + self.name + "/" + data["level"] + "/"
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        imgPath = file_path + data['name'] + ".png"
        data["imgUrl"] = imgUrl
        data["imgPath"] = imgPath
        data["imgName"] = data['name'] + ".png"
        sess = requests.Session()
        headers = {}
        headers["User-Agent"] = random.choice(agents)
        try:
            try:
                file_data = sess.get(imgUrl, timeout=10, headers=headers).content
            except:
                file_data = sess.get(imgUrl, timeout=10, headers=headers).content
            with open(imgPath, "wb") as fd:
                fd.write(file_data)
        except:
            pass
        item = ExpertItem()
        for key, val in data.items():
            # print key
            item[key] = val
        yield item





