# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
from Academician.items import CasadItem, CkcestItem

class AcademicianPipeline(object):

    def __init__(self):
        # client = MongoClient("10.4.255.129", 27017)
        client = MongoClient("192.168.20.102", 27017)
        Acad = client["Academician"]
        self.casad = Acad['Casad']
        self.ckcest = Acad['Ckcest']


    def process_item(self, item, spider):
        if isinstance(item, CasadItem):
            try:
                # print dict(item)
                self.casad.insert(dict(item))
            except Exception, e:
                print e
        if isinstance(item, CkcestItem):
            try:
                # print dict(item)
                self.ckcest.insert(dict(item))
            except Exception, e:
                print e
