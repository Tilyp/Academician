#! -*- coding: utf-8 -*-
import json
import os
import re
from scrapy import Request, FormRequest
from scrapy.spiders import CrawlSpider
from bs4 import BeautifulSoup
import requests
from Academician.items import CkcestItem


class ExpertCkcest(CrawlSpider):
    name = "ExpertCkcest"
    host = "http://ysg.ckcest.cn"
    keyword = ["旅游业", "高效农业", "互联网产业", "医疗健康产业", "金融服务业",
               "会展业", "现代物流业", "油气产业", "医药产业", "低碳制造业",
               "房地产业", "高新技术教育文化体育产业"]

    post_url = "http://expert.ckcest.cn/api/queryClaimExperts"

    def start_requests(self):
        data = {"name": "", "institute": "", "subject": "", "keyword": "房地产业", "from": "0", "size": "16"}
        for key in self.keyword[1:2]:
            data["keyword"] = key
            yield FormRequest(url=self.post_url, formdata=data, meta={"data": data},
                              callback=self.parse, dont_filter=True)

    def parse(self, response):
        soup = json.loads(response.body)
        data = response.meta["data"]
        for obj in soup["obj"]:
            print len(obj.keys())
            obj = {"altName":"王一江;wang yi jiang;wang,yj;yijiang wang;yijiang,wang;wang,yijiang;yj,wang;",
                "altOrganization":"tsinghua university;tsinghua univ;清华大学;",
                "avatarUrl":"null",
                "ccd":"null",
                "city":"北京市",
                "clc":"null",
                "degree":"null",
                "department":"null",
                "displayNo":"null",
                "domain":"null",
                "gender":"null",
                "introduction":"null",
                "isCore":"null",
                "isExact":"false",
                "isFirst":"null",
                "isMerged":"true",
                "isShown":"true",
                "isValid":"true",
                "kId":"BEAC906A-D667-B898-DD0C-1C2D9E282CCB",
                "keyword":"腐败程度;微观分析;权力寻租;房地产业;投资决定机制;实际控制人;利率;内螺纹;应力集中;疲劳强度;安全系数;螺纹根部;最大应力",
                "name":"王一江",
                "nativePlace":"null",
                "operateTime":"1494363029330",
                "organization":"清华大学",
                "pinyin":"wang yi jiang",
                "position":"null",
                "positionalTitle":"null",
                "profession":"null",
                "province":"北京",
                "researchDirection":"null",
                "resume":"null",
                "subject":"政治学;国民经济学;金融学;机械工程;力学",
                "technicalName":"null", "thirdIdentifier": "null", "thirdNo": "null", "weight": "null"}
            detail = {"nameOrgArray": str([obj])}
            print detail
            base_url = "http://expert.ckcest.cn/api/queryExpertSummary"
            yield FormRequest(url=base_url, formdata=detail, meta={"data": detail},
                              callback=self.parse_summary, dont_filter=True)
            break
            kId = obj["kId"]
            name = obj["name"]
            subject = obj["subject"]
            keyword = obj["keyword"].strip()
            organization = obj["organization"]
        count = soup["count"]
        if int(data["from"]) < count:
            data["from"] = str(int(data["from"]) + 16)
            # yield FormRequest(url=self.post_url, formdata=data, meta={"data": data},
            #                   callback=self.parse, dont_filter=True)



    def parse_summary(self, response):
        """'根据数据搜索表明' + $scope.curExpert.name + '（专家）可见的最早中文论文发表是'
                            + chineseDetailData.year + '年在' + chineseDetailData.journal + '（期刊）上的'
                            + chineseDetailData.title + '一文，最早英文论文发表是' + englishDetailData.year + '年在'
                            + englishDetailData.journal + '（期刊）上的' + englishDetailData.title + '一文。'
                            + '截至' + $scope.summaryData.year + '年在' + sourceStr + '等' + categoryCount
                            + '种期刊上共发文' + totalCount + '篇，其研究领域主要集中在' + areaStr + '等方向。'"""
        soup = json.loads(response.body)
        print json.dumps(soup, ensure_ascii=False)


