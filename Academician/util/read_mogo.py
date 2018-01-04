#! -*- coding: utf-8 -*-
import json

import xlwt
from pymongo import MongoClient


class Read_mongo(object):

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
        self.HkPeople = Acad['HkPeopleItem']
        self.Kgxj = Acad['Kgxj']
        self.Expert = Acad['ExpertItem']
        self.CkcestSearch = Acad['CkcestSearchItem']
        self.HnPeople = Acad['HnPeopleItem']
    def read_casad(self):
        workbook = xlwt.Workbook(encoding='utf-8')
        worksheet = workbook.add_sheet(u'sheet1', cell_overwrite_ok=True)
        title_row = 0
        col = 1
        key_list = []
        for i in self.HnPeople.find():
            if title_row == 0:
                for key in i.keys():
                    if key != "_id":
                        key_list.append(key)
                        worksheet.write(0, title_row, label=key)
                        title_row += 1
            row = 0
            for keys in key_list:
                val = json.dumps(i[keys], ensure_ascii=False)
                worksheet.write(col, row, label=val)
                row += 1
            col += 1
        workbook.save('HnPeople.xls')

if __name__ == "__main__":
    Read_mongo().read_casad()