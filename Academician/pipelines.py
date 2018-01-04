# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
from Academician.items import CasadItem, CkcestItem, WsspItem, \
    HkwbItem, NgdsbItem, DostItem, DostOthItem, IitbXxgkItem, IitbZwgkItem, \
    KgxjItem, HkPeopleItem, ExpertItem, HnPeopleItem, CkcestSearchItem


class AcademicianPipeline(object):

    def __init__(self):
        client = MongoClient("192.168.20.102", 27017)
        Acad = client["Academician"]
        self.casad = Acad['CasadRe']
        self.ckcest = Acad['CkcestRe']
        self.wssp = Acad['WsspItemkeji']
        self.hkwb = Acad['Hkwb']
        self.ngdsb = Acad['Ngdsb']
        self.dost = Acad['DostItem']
        self.dostOth = Acad['DostOthItem']
        self.Zwgk = Acad['IitbZwgkItem']
        self.Xxgk = Acad['IitbXxgkItem']
        self.Kgxj = Acad['Kgxj']
        self.HkPeople = Acad['HkPeopleItem']
        self.Expert = Acad['ExpertItem']
        self.HnPeople = Acad['HnPeopleItem']
        self.CkcestSearch = Acad['CkcestSearchItem']



    def process_item(self, item, spider):
        if isinstance(item, CkcestSearchItem):
            try:
                self.CkcestSearch.insert(dict(item))
            except Exception, e:
                print e
        if isinstance(item, HnPeopleItem):
            try:
                self.HnPeople.insert(dict(item))
            except Exception, e:
                print e
        if isinstance(item, ExpertItem):
            try:
                self.Expert.insert(dict(item))
            except Exception, e:
                print e
        if isinstance(item, HkPeopleItem):
            try:
                self.HkPeople.insert(dict(item))
            except Exception, e:
                print e
        if isinstance(item, KgxjItem):
            try:
                self.Kgxj.insert(dict(item))
            except Exception, e:
                print e
        if isinstance(item, IitbXxgkItem):
            try:
                self.Xxgk.insert(dict(item))
            except Exception, e:
                print e
        if isinstance(item, IitbZwgkItem):
            try:
                self.Zwgk.insert(dict(item))
            except Exception, e:
                print e
        if isinstance(item, DostOthItem):
            try:
                self.dostOth.insert(dict(item))
            except Exception, e:
                print e
        if isinstance(item, DostItem):
            try:
                self.dost.insert(dict(item))
            except Exception, e:
                print e
        if isinstance(item, NgdsbItem):
            try:
                self.ngdsb.insert(dict(item))
            except Exception, e:
                print e
        if isinstance(item, HkwbItem):
            try:
                self.hkwb.insert(dict(item))
            except Exception, e:
                print e
        if isinstance(item, WsspItem):
            try:
                self.wssp.insert(dict(item))
            except Exception, e:
                print e
        if isinstance(item, CasadItem):
            try:
                self.casad.insert(dict(item))
            except Exception, e:
                print e
        if isinstance(item, CkcestItem):
            try:
                self.ckcest.insert(dict(item))
            except Exception, e:
                print e

