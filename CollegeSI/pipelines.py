# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from twisted.enterprise import adbapi
import pymysql
from pymysql import cursors 
class CollegesiPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(
            host='localhost',
            db='collegesi',
            user='root',
            passwd='DWY5201314',
            charset='utf8'
        )
        self.conn.autocommit(True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        sql = '''
        insert into collegesi(
            major,
            href,
            positiontitle,
            companyname,
            placeofwork,
            salary,
            releasetime,
            briefintroduction,
            corporatewelfare,
            jobinformation,
            functionalcategories,
            keyword,
            companyinformation) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            '''
        data = (
            item['Major'],
            item['Href'],
            item['PositionTitle'],
            item['CompanyName'],
            item['PlaceOfWork'],
            item['Salary'],
            item['ReleaseTime'],
            item['BriefIntroduction'],
            item['CorporateWelfare'],
            item['JobInformation'],
            item['FunctionalCategories'],
            item['Keyword'],
            item['CompanyInformation']
            )
        print("------------------Piplines------------------\n")
        try:
            self.cursor.execute(sql,data)
            print(item['PositionTitle'] + "--------插入成功-------" + "\n")
        except Exception as e:
            print(e)
            self.conn.rollback()

            
