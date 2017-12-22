#! -*- coding: utf-8 -*-
import json
import os
import re

from requests import ConnectionError
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
        # for xb in [7055] + range(3532, 3541)[1:2]:
        for xb in range(3532, 3541)[7:8]:
            data = self.data
            data["xbType"] = str(xb)
            yield FormRequest(url=self.post_url, formdata=data, callback=self.parse, meta={"data": data}, dont_filter=True)
            # break

    def parse(self, response):
        soup = BeautifulSoup(response.body, "lxml")
        links = soup.find("div", {"id": "acInfoId"}).find_all("a")
        for link in links:
            base_url = self.host + link["href"]
            detail = {"url": base_url}
            req_url = base_url + "&pagename=grxx_jbxx&flag=0"
            yield Request(url=req_url, callback=self.parse_home, meta={"data": detail}, dont_filter=True)
            # break
        data = response.meta["data"]
        current_page = data["default_current_page_param_name"]
        data["default_current_page_param_namec"] = current_page
        data["default_current_page_param_name"] = str(int(current_page) + 1)
        data["default_get_page_by_perpage"] = "y"
        href = soup.find("div", class_="gy_right_feny").find_all("a")[-1]["href"]
        totalPage = re.findall("\d+", href)[0]
        if int(totalPage) > int(current_page.strip()):
            yield FormRequest(url=self.post_url, formdata=data, callback=self.parse, meta={"data": data}, dont_filter=True)

    def parse_home(self, response):
        soup = BeautifulSoup(response.body, "lxml")
        resume = soup.find("div", class_="jxym_nr").get_text(strip=True)
        jxym = soup.find("div", class_="jxym")
        imgUrl = self.host + jxym.find("img")["src"]
        identity = soup.find("div", class_="jxy_toptit yhei").get_text(strip=True).split(u" · ")[0]
        jxym_text = jxym.find_all("li")
        keyword = {u"姓名": "Name", u"民族": "Nation", u"性别": "Sex", u"国籍": "Country", u"籍贯": "Ancestral",
                   u"出生日期": "Birthday", u"去世日期": "DeathTime", u"所属党派":"Party",
                   u"当选院士年份": "ElectedTime", u"毕业院校": "University", u"学部学科": "Department"}
        detail = response.meta["data"]
        for text in jxym_text:
            key = text.find("h3").get_text(strip=True)
            msg = text.find("h4").get_text(strip=True).replace("\r\n", "").replace("\t", "")
            detail[keyword[key]] = msg
        for key, value in keyword.items():
            if not detail.has_key(value):
                detail[value] = "Null"
        file_path = "data/" + self.name + "/" + identity + "/"
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        imgPath = file_path + detail["Name"] + ".png"
        detail["imgPath"] = imgPath
        detail["imgUrl"] = imgUrl
        detail["resume"] = resume
        detail["identity"] = identity
        sess = requests.Session()
        try:
            file_data =sess.get(imgUrl, timeout=10).content
        except ConnectionError:
            file_data = sess.get(imgUrl, timeout=10).content
        with open(imgPath, "wb") as fd:
            fd.write(file_data)
        # print json.dumps(dict(detail), ensure_ascii=False)
        req_url = detail['url'] + "&pagename=grxx_zyxl&flag=1"
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
        grxx = soup.find("ul", {"id": "grxx"}).find_all("li")
        if len(grxx) == 4:
            req_url = detail["url"] + "&pagename=grxx_shzw&flag=3"
            yield Request(url=req_url, callback=self.parse_main_duties, meta={"data": detail})
        else:
            detail["Social_duties"] = []
            detail["plurality"] = []
            item = CkcestItem()
            for key, value in detail.items():
                item[key] = value
            # print json.dumps(dict(item), ensure_ascii=False)
            yield item

    def parse_main_duties(self, response):
        soup = BeautifulSoup(response.body, "lxml")
        keyword = {u"社会职务": "Social_duties", u"主要兼职": "plurality"}
        nrtab1_tit = soup.find_all("div", class_="jxym_nrtab1_tit")
        detail = response.meta["data"]
        nrtab1 = soup.find_all("div", class_="jxym_nrtab1_n")
        for index, tabl in enumerate(nrtab1):
            key = nrtab1_tit[index].get_text(strip=True)
            detail[keyword[key]] = []
            for nrt in tabl.find_all("tr")[1:]:
                exp = []
                for td in nrt.find_all("td"):
                    con = td.get_text(strip=True)
                    if con:
                        exp.append(con)
                    else:
                        exp.append("Null")
                detail[keyword[key]].append(exp)
        if not detail.has_key("Social_duties"):
            detail["Social_duties"] = []
        if not detail.has_key("plurality"):
            detail["plurality"] = []
        item = CkcestItem()
        for key, value in detail.items():
            item[key] = value
        # print json.dumps(dict(item), ensure_ascii=False)
        yield item
