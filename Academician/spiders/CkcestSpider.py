#! -*- coding: utf-8 -*-
import json
import os
import re
from scrapy import Request, FormRequest
from scrapy.spiders import CrawlSpider
from bs4 import BeautifulSoup
import requests
from Academician.items import CkcestItem


class CkcestSpider(CrawlSpider):
    name = "CkcestSpider"
    host = "http://ysg.ckcest.cn"
    post_url = "http://ysg.ckcest.cn/cae/ysgIndexAction.do?method=index"
    data = {
        "ename": "",
        "xbType": "3535",
        "searchTypeYS": "",
        "searchType": "",
        "flag": "0",
        "keyword": "",
        "becomeYear": "",
        "sex": "",
        "country": "9",
        "departmentArea": "",
        "nation": "",
        "default_current_page_param_namec": "2",
        "default_current_page_param_name": "1",
        "default_page_size_param_name": "12",
        "default_get_page_by_perpage": "12"
    }

    def start_requests(self):
        for xb in range(3532, 3541) + [7055]:
            data = self.data
            data["xbType"] = str(xb)
            yield FormRequest(url=self.post_url, formdata=data, callback=self.parse, meta={"data": data}, dont_filter=True)

    def parse(self, response):
        soup = BeautifulSoup(response.body, "lxml")
        links = soup.find("div", {"id": "acInfoId"}).find_all("a")
        for link in links:
            req_url = self.host + link["href"]
            yield Request(url=req_url, callback=self.parse_home, dont_filter=True)
            break
        data = response.meta["data"]
        current_page = data["default_current_page_param_name"]
        data["default_current_page_param_namec"] = current_page
        data["default_current_page_param_name"] = str(int(current_page) + 1)
        data["default_get_page_by_perpage"] = "y"
        href = soup.find("div", class_="gy_right_feny").find_all("a")[-1]["href"]
        totalPage = re.findall("\d+", href)[0]
        if totalPage < int(current_page):
            yield FormRequest(url=self.post_url, formdata=data, callback=self.parse, meta={"data": data}, dont_filter=True)

    def parse_home(self, response):
        soup = BeautifulSoup(response.body, "lxml")
        resume = soup.find("div", class_="jxym_nr").get_text(strip=True)
        jxym = soup.find("div", class_="jxym")
        imgUrl = self.host + jxym.find("img")["src"]
        identity = soup.find("div", class_="jxy_toptit yhei").get_text(strip=True).split(u" · ")[0]
        jxym_text = jxym.find_all("h4")
        keyword = ["Name", "Nation", "Sex", "Country", "Ancestral", "Birthday", "ElectedTime", "University", "Department"]
        detail = {}
        for i, text in enumerate(jxym_text):
            detail[keyword[i]] = text.get_text(strip=True).replace("\r\n", "").replace("\t", "")
        # print json.dumps(dict(detail), ensure_ascii=False)
        file_path = "data/" + self.name + "/" + identity + "/"
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        imgPath = file_path + detail["Name"] + ".png"
        detail["imgPath"] = imgPath
        detail["imgUrl"] = imgUrl
        detail["resume"] = resume
        detail["identity"] = identity
        detail["url"] = response.url
        file_data = requests.get(imgUrl).content
        with open(imgPath, "wb") as fd:
            fd.write(file_data)
        req_url = response.url + "&pagename=grxx_zyxl&flag=1"
        yield Request(url=req_url, callback=self.parse_edu, meta={"data": detail})

    def parse_edu(self, response):
        soup = BeautifulSoup(response.body, "lxml")
        nrtab1 = soup.find("div", class_="jxym_nrtab1_n")
        detail = response.meta["data"]
        detail["Education"] = []
        for nrt in nrtab1.find_all("tr")[1:]:
            edu = []
            for td in nrt.find_all("td"):
                con = td.get_text(strip=True)
                if con:
                    edu.append(con)
                else:
                    edu.append("Null")
            detail["Education"].append(edu)
        req_url = detail["url"] + "&pagename=grxx_zyjl&flag=2"
        yield Request(url=req_url, callback=self.parse_experience, meta={"data": detail})

    def parse_experience(self, response):
        soup = BeautifulSoup(response.body, "lxml")
        nrtab1 = soup.find("div", class_="jxym_nrtab1_n")
        detail = response.meta["data"]
        detail["Experience"] = []
        for nrt in nrtab1.find_all("tr")[1:]:
            exp = []
            for td in nrt.find_all("td"):
                con = td.get_text(strip=True)
                if con:
                    exp.append(con)
                else:
                    exp.append("Null")
            detail["Experience"].append(exp)
        item = CkcestItem()
        for key, value in detail.items():
            item[key] = value

        # print json.dumps(dict(item), ensure_ascii=False)
        yield item