#! -*- coding: utf-8 -*-

from scrapy import cmdline

# cmdline.execute("scrapy crawl CasadSpider --logfile log/CasadSpider.log".split())
# cmdline.execute("scrapy crawl CasadSpider ".split())

# cmdline.execute("scrapy crawl CkcestSpider --logfile log/CkcestSpider.log".split())
# cmdline.execute("scrapy crawl CkcestSpider".split())

# cmdline.execute("scrapy crawl ExpertCkcest".split())
# cmdline.execute("scrapy crawl ExpertCkcest --logfile log/ExpertCkcest.log".split())

cmdline.execute("scrapy crawl WsspSpider".split())


