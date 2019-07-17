# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CollegesiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Major = scrapy.Field()                 #专业(自定义字段，非需要爬取内容)

    Href  =  scrapy.Field()              #职位链接

    PositionTitle = scrapy.Field()       #职位名

    CompanyName = scrapy.Field()         #公司名

    PlaceOfWork = scrapy.Field()         #工作地点

    Salary  = scrapy.Field()                #薪资

    ReleaseTime  = scrapy.Field()           #发布时间

    BriefIntroduction  = scrapy.Field()     #简介（学历要求、工作仅有要求等）

    CorporateWelfare  = scrapy.Field()      #公司福利(年终奖、五险一金等)

    JobInformation  = scrapy.Field()        #职位信息

    FunctionalCategories = scrapy.Field()    #职能类别

    Keyword = scrapy.Field()                  #关键字

    CompanyInformation  = scrapy.Field()    #公司信息
    
