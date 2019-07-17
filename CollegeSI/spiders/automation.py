# -*- coding: utf-8 -*-
import scrapy
from CollegeSI.items import CollegesiItem


class AutomationSpider(scrapy.Spider):
    name = 'automation'
    allowed_domains = ['search.51job.com']
    start_urls = ['https://search.51job.com/list/000000,000000,0000,00,9,99,%25E8%2587%25AA%25E5%258A%25A8%25E5%258C%2596,2,1.html?']

    def parse(self, response):
        resultList = response.xpath("//div[@class='el']")
        i=1
        for result in resultList:
            item = CollegesiItem()
            item['Major'] = '自动化'
            item['Href'] = result.xpath("//p[@class='t1']/span/a/@href").extract()
            item['PositionTitle'] = result.xpath("./p[@class='t1']/span/a/text()").extract()
            item['CompanyName'] = result.xpath("./span[@class='t2']/a/text()").extract()
            item['PlaceOfWork'] = result.xpath("./span[@class='t3']/text()").extract()
            item['Salary'] = result.xpath("./span[@class='t4']/text()").extract()
            item['ReleaseTime'] = result.xpath("./span[@class='t5']/text()").extract()
            i += 1

            yield scrapy.Request(item['Href'],meta={'item':item},callback=self.detail_parse,dont_filter=True)

        NextPageUrl = 'https://search.51job.com/list/000000,000000,0000,00,9,99,%25E8%2587%25AA%25E5%258A%25A8%25E5%258C%2596,2,'+str(i)+'.html?'
        #NextPageUrl = response.xoath("//div[@class='dw_page']//li[@class='bk'][1]/a/@href").extract()

        if NextPageUrl is not None:
            yield scrapy.Request(NextPageUrl,callback=self.parse,dont_filter=True)
        return None


    def detail_parse(self,response):
        item = response.meta['item']

        item['BriefIntroduction'] = response.xpath("//div[@class='tHeader tHjob']//p[@class='msg ltype']/@title").extract()
        CorporateWelfares = response.xpath("//div[@class='tHeader tHjob']//div[@class='jtag']/div[@class='t1']/span[@class='sp4']")
        item['CorporateWelfare'] = ''
        for CorporateWelfare in CorporateWelfares:
            item['CorporateWelfare'] += CorporateWelfare.xpath("./text()").extract()
            item['CorporateWelfare'] += ' | '

        tBorderTop_box = response.xpath("//div[@class='tCompany_main']/div[@class='tBorderTop_box']")

        JobInformations = tBorderTop_box[0].xpath("./div[@class='bmsg job_msg inbox']/p")
        item['JobInformation'] = ''
        for JobInformation in JobInformations:
            item['JobInformation'] += JobInformation.xpath("string(.)").strip()
            item['JobInformation'] += '<br/>'
        
        FunctionalCategorieses = tBorderTop_box[0].xpath("./div[@class='bmsg job_msg inbox']/div[@class='mt10']/p[0]/a")
        item['FunctionalCategories'] = ''
        for FunctionalCategories in FunctionalCategorieses:
            item['FunctionalCategories'] += FunctionalCategories.xpath("string(.)").strip()
            item['FunctionalCategories'] += '|'
        
        Keywords = tBorderTop_box[0].xpath("./div[@class='bmsg job_msg inbox']/div[@class='mt10']/p[1]/a")
        item['Keyword'] = ''
        for Keyword in Keywords:
            item['Keyword'] += Keyword.xpath("string(.)").strip()
            item['Keyword'] += '|'

        item['CompanyInformation'] = tBorderTop_box[2].xpath("./div[@class='tmsg inbox']/text()").extract()

        return item

            