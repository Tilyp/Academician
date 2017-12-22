#! -*- coding: utf-8 -*-
import json
import os
import random
from requests import ConnectionError
from scrapy import Request, FormRequest
from scrapy.spiders import CrawlSpider
from bs4 import BeautifulSoup
import requests
from Academician.items import WsspItem
from Academician.user_agents import agents

class WsspSpider(CrawlSpider):
    name = "WsspSpider"
    host = "http://wssp.hainan.gov.cn"
    base_url = "http://wssp.hainan.gov.cn/wssp/hn/module/wssp/wssb/sbindex.do"

    def start_requests(self):

        data = {"acc_id": "", "bmmc": "", "ddid": "HZ2881f4424539dd0142453d7336002c",
                "deptId": "HZ2881f4424539dd0142453d7336002c", "sxlx": "", "sxname": "",
                "HZ_PAGE_NO": "1", "HZ_PAGE_SIZE": "10", "pageNum": ""}
        yield FormRequest(url=self.base_url, formdata=data, meta={"data": data}, callback=self.parse)

        """
        # req_url = "http://wssp.hainan.gov.cn/wssp/hn/module/wssp/wssb/getSXJS.do?id=22357cf211944df5b0a0dee77ecddd94"
        req_url = "http://wssp.hainan.gov.cn/wssp/hn/module/wssp/wssb/getSXJS.do?id=810c3c84f8084eab97a80ad12be00933&zh_id="
        # req_url = "http://wssp.hainan.gov.cn/wssp/hn/module/wssp/wssb/getSXJS.do?id=65b3162aed174f82b86538134f1db578"
        yield Request(url=req_url, callback=self.parse_hn, dont_filter=True)
        """

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
            yield FormRequest(url=self.base_url, formdata=data, meta={"data": data}, callback=self.parse)

    def parse_hn(self, response):
        soup = BeautifulSoup(response.body, "lxml")
        temp_main = soup.find("div", class_="public_temp_main_1 fn-clear")
        lawGuide_mainTit = temp_main.find("div", class_="lawGuide_mainTit fn-clear")
        item_num = lawGuide_mainTit.get_text(strip=True).split("\n")[-1].split(u":")[1].split(u"网上")[0]
        lawGuide_mainLeft = temp_main.find("div", class_="lawGuide_mainLeft")
        lawGuide_mainLeft_tit = lawGuide_mainLeft.find("div", class_="lawGuide_mainLeft_tit").get_text()
        base_msg = lawGuide_mainLeft.find("ul", class_="fn-clear").find_all("li")
        base_key = {u"办理地点": "HandleAddress", u"办理时间": "HandleTime", u"咨询电话": "AskTell", u"投诉电话":"complain"}
        detail = {}
        detail["item_num"] = item_num
        detail["url"] = response.url
        detail["ServiceDepartment"] = lawGuide_mainLeft_tit
        for msg in base_msg:
            key = msg.find("h2").get_text(strip=True)
            value = msg.find("span").get_text(strip=True)
            if value == "":
                value = "Null"
            detail[base_key[key]] = value
        lawGuide_main = soup.find("ul", class_="lawGuide_main").find_all("li")
        main_key = ["item_name", "BidSubject", "HandleResults", "PromiseTime", "LegalTime"]
        detail["otherPLTime"] = []
        for ind, law in enumerate(lawGuide_main):
            val = law.get_text(strip=True).split(u"：")[1]
            if val == "":
                val = "Null"
            try:
                detail[main_key[ind]] = val
            except:
                detail["otherPLTime"].append(law.get_text(strip=True))
        sqtj = soup.find("div", {"id": "sqtj"}).find("font").get_text(strip=True)
        if sqtj == "":
            sqtj = "Null"
        detail['HandleCondition'] = sqtj
        divchange = soup.find("div", {"id": "divchange"}).find_all("tr")
        detail["Rereq"] = []
        MaterialReq = {}
        lentr = len(divchange[1:])
        if lentr == 0:
            MaterialReq["Material"] = []
            MaterialReq['MaterialDemand'] = "Null"
            detail["Rereq"].append(MaterialReq)
        rereq = ["Serial", "MaterialName", "MaterialFlag"]
        for indtr, tr in enumerate(divchange[1:]):
            tds = tr.find_all("td")
            if len(tds) == 2:
                MaterialDemand = tds[1].get_text(strip=True)
                if MaterialReq != {}:
                    detail["Rereq"].append(MaterialReq)
                    # print json.dumps(MaterialReq, ensure_ascii=False)
                    MaterialReq = {}
                MaterialReq["Material"] = []
                MaterialReq['MaterialDemand'] = MaterialDemand
            elif indtr == 0 and len(tds) != 2:
                MaterialReq = {}
                MaterialReq["Material"] = []
                MaterialReq['MaterialDemand'] = " "
                Material = {}
                for ind, val in enumerate(tds[1:]):
                    Material[rereq[ind]] = val.get_text(strip=True)
                MaterialReq["Material"].append(Material)
            else:
                Material = {}
                for ind, val in enumerate(tds[1:]):
                    Material[rereq[ind]] = val.get_text(strip=True)
                MaterialReq["Material"].append(Material)
            if indtr + 1 == lentr:
                # print json.dumps(MaterialReq, ensure_ascii=False)
                detail["Rereq"].append(MaterialReq)
        basis = soup.find("div", class_="basis yellow_tab").find_all("tr")
        detail["HandleBasis"] = []
        flag = 1
        dsa = {}
        for i in basis:
            tds = i.find_all("td")
            if flag / 2 == 0:
                dsa = {}
                dsa["BasisName"] = tds[1].get_text(strip=True)
                try:
                    basis = tds[1].find("a")
                    dsa["BasisUrl"] = basis["href"]
                except:
                    dsa["BasisUrl"] = "Null"
            elif flag / 2 == 1:
                Description = tds[1].get_text(strip=True)
                if Description == "":
                    Description = "Null"
                dsa["BasisDescription"] = Description
                detail["HandleBasis"].append(dsa)
            flag += 1
        column_tabs = soup.find("div", class_="column_tabs").find_all("li")
        if len(column_tabs) > 2:
            req_file = column_tabs[-1]["onclick"].split("'")[1]
            next_url = self.host + req_file
            yield Request(url=next_url, callback=self.parse_file, meta={"data": detail})
        else:
            item = WsspItem()
            detail["fileMsg"] = []
            for key, val in detail.items():
                item[key] = val
            yield item
            # print item

    def parse_file(self, response):
        detail = response.meta["data"]
        soup = BeautifulSoup(response.body, "lxml")
        trs = soup.find("table", class_="list_form").find_all("tr")
        detail["fileMsg"] = []
        for tr in trs[1:]:
            file_msg = {}
            tds = tr.find_all("td")
            fileAuth = tds[1].get_text(strip=True)
            fileName = tds[2].get_text(strip=True)
            fileId = tds[3].find("a")["href"].split("'")[-2]
            file_base_url = "http://wssp.hainan.gov.cn/wssp/downloadFileWssp.do?id=%s"
            fileUrl = file_base_url % fileId
            sess = requests.Session()
            try:
                file_data = sess.get(fileUrl, timeout=10).content
            except ConnectionError:
                file_data = sess.get(fileUrl, timeout=10).content
            file_path = "data/" + self.name + "/" + detail["item_num"] + "/"
            if not os.path.exists(file_path):
                os.makedirs(file_path)
            filePath = file_path + fileName
            with open(filePath, "wb") as fd:
                fd.write(file_data)
            file_msg["fileUrl"] = fileUrl
            file_msg["filePath"] = filePath
            file_msg["fileName"] = fileName
            file_msg["fileAuth"] = fileAuth
            detail["fileMsg"].append(file_msg)
        item = WsspItem()
        for key, val in detail.items():
            item[key] = val
        yield item
        # print item



    def get_data(self, url):
        sess = requests.Session()
        agent = random.choice(agents)
        header = {"User-Agent": agent}
        html = sess.get(url, timeout=10, headers=header,)
        html.encoding = "GBK"
        soup = BeautifulSoup(html.text, "lxml")
        try:
            print soup.find("div", {"id": "Zoom"}).get_text(strip=True)
        except:
            print url
