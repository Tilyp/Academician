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

class HkwbItem(scrapy.Field):
    url = scrapy.Field()
    content = scrapy.Field()
    dataTime = scrapy.Field()
    title = scrapy.Field()

class NgdsbItem(scrapy.Field):
    url = scrapy.Field()
    content = scrapy.Field()
    dataTime = scrapy.Field()
    title = scrapy.Field()

class DostItem(scrapy.Field):
    Publisher = scrapy.Field()
    url = scrapy.Field()
    openTime = scrapy.Field()
    fileMsg = scrapy.Field()
    title = scrapy.Field()
    pushTime = scrapy.Field()
    content = scrapy.Field()
    DocumentNum = scrapy.Field()
    indexNum = scrapy.Field()
    keyword = scrapy.Field()

class DostOthItem(scrapy.Field):
    fileMsg = scrapy.Field()
    keyword = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    pushTime = scrapy.Field()
    content = scrapy.Field()
    infoSource = scrapy.Field()

class IitbXxgkItem(scrapy.Field):
    content = scrapy.Field()
    group = scrapy.Field()
    fileMsg = scrapy.Field()
    keyword = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    agency = scrapy.Field()
    pushTime = scrapy.Field()
    topic = scrapy.Field()
    topicWord = scrapy.Field()
    DocumentNum = scrapy.Field()
    indexNum = scrapy.Field()
    imgMsg = scrapy.Field()

class IitbZwgkItem(scrapy.Field):
    url = scrapy.Field()
    fileMsg = scrapy.Field()
    content = scrapy.Field()
    imgMsg = scrapy.Field()
    keyword = scrapy.Field()
    title = scrapy.Field()

class KgxjItem(scrapy.Field):
    keyword = scrapy.Field()
    author = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    pushTime = scrapy.Field()
    content = scrapy.Field()
    source = scrapy.Field()
    imgMsg = scrapy.Field()

class HkPeopleItem(scrapy.Field):
    content = scrapy.Field()
    keyword = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    author = scrapy.Field()
    webName = scrapy.Field()
    source = scrapy.Field()
    flag = scrapy.Field()
    undateTime = scrapy.Field()
    imgMsg = scrapy.Field()

class ExpertItem(scrapy.Field):
    imgName = scrapy.Field()
    name = scrapy.Field()
    keyword = scrapy.Field()
    level = scrapy.Field()
    imgPath = scrapy.Field()
    content = scrapy.Field()
    organization = scrapy.Field()
    kId = scrapy.Field()
    imgUrl = scrapy.Field()
    subject = scrapy.Field()

class HnPeopleItem(scrapy.Field):
    keyword = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    baseUrl = scrapy.Field()
    pushTime = scrapy.Field()
    content = scrapy.Field()
    editor = scrapy.Field()
    imgMsg = scrapy.Field()

class CkcestSearchItem(scrapy.Field):
    name = scrapy.Field()
    resume = scrapy.Field()
    SelectedTime = scrapy.Field()
    Ancestral = scrapy.Field()
    Nation = scrapy.Field()
    Birthday = scrapy.Field()
    Country = scrapy.Field()
    Department = scrapy.Field()
    Party = scrapy.Field()
    sex = scrapy.Field()
    subject = scrapy.Field()