# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AcademicianItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class CasadItem(scrapy.Item):
    name = scrapy.Field()
    imgPath = scrapy.Field()
    url = scrapy.Field()
    imgUrl = scrapy.Field()
    resume = scrapy.Field()
    identity = scrapy.Field()


class CkcestItem(scrapy.Item):
    Education = scrapy.Field()
    Experience = scrapy.Field()
    Name = scrapy.Field()
    resume = scrapy.Field()
    url = scrapy.Field()
    Country = scrapy.Field()
    ElectedTime = scrapy.Field()
    Ancestral = scrapy.Field()
    imgPath = scrapy.Field()
    Sex = scrapy.Field()
    Birthday = scrapy.Field()
    identity = scrapy.Field()
    Department = scrapy.Field()
    Nation = scrapy.Field()
    University = scrapy.Field()
    imgUrl = scrapy.Field()
    DeathTime = scrapy.Field()
    Party = scrapy.Field()
    Social_duties = scrapy.Field()
    plurality = scrapy.Field()


class WsspItem(scrapy.Item):
    LegalTime = scrapy.Field()
    otherPLTime = scrapy.Field()
    Rereq = scrapy.Field()
    HandleAddress = scrapy.Field()
    item_name = scrapy.Field()
    BidSubject = scrapy.Field()
    HandleBasis = scrapy.Field()
    complain = scrapy.Field()
    HandleResults = scrapy.Field()
    HandleCondition = scrapy.Field()
    item_num = scrapy.Field()
    PromiseTime = scrapy.Field()
    AskTell = scrapy.Field()
    ServiceDepartment = scrapy.Field()
    HandleTime = scrapy.Field()
    fileUrl = scrapy.Field()
    fileName = scrapy.Field()
    fileAuth = scrapy.Field()
    filePath = scrapy.Field()
    url = scrapy.Field()
    fileMsg = scrapy.Field()