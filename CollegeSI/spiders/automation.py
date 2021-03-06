# -*- coding: utf-8 -*-
import scrapy
from CollegeSI.items import CollegesiItem


class AutomationSpider(scrapy.Spider):
    name = 'automation'
    allowed_domains = ['search.51job.com']
    start_urls = ['https://search.51job.com/list/000000,000000,0000,00,9,99,%25E8%2587%25AA%25E5%258A%25A8%25E5%258C%2596,2,1.html']

    def parse(self, response):
        resultList = response.xpath("//div[@class='dw_wp']/div[@id='resultList']/div[@class='el']")
        for result in resultList:
            item = CollegesiItem()
            item['Major'] = '自动化'
            item['Href'] = result.xpath(".//p/span/a/@href").extract()[0]
            item['PositionTitle'] = result.xpath(".//p/span/a/text()").extract()[0]
            item['CompanyName'] = result.xpath(".//span[@class='t2']/a/text()").extract()[0]
            item['PlaceOfWork'] = result.xpath(".//span[@class='t3']/text()").extract()[0]
            Salary = result.xpath(".//span[@class='t4']/text()").extract()
            if Salary:
                item['Salary'] = Salary[0]
            else:
                item['Salary'] = None
            item['ReleaseTime'] = result.xpath(".//span[@class='t5']/text()").extract()[0]


            #print(item['PositionTitle'])

            yield scrapy.Request(item['Href'],meta={'item':item},callback=self.detail_parse,dont_filter=True)

        NextPageUrl = response.xpath("//div[@class='dw_page']//li[@class='bk'][2]/a/@href").extract()[0]

        if NextPageUrl is not None:
            yield scrapy.Request(NextPageUrl,callback=self.parse,dont_filter=True)
       # return None
    def detail_parse(self,response):
        item = response.meta['item']

        BriefIntroduction = response.xpath("//div[@class='tHeader tHjob']//p[@class='msg ltype']/@title").extract()
        if BriefIntroduction:
            item['BriefIntroduction'] = BriefIntroduction
        else:
            item['BriefIntroduction'] = None


        CorporateWelfares = response.xpath("//div[@class='tHeader tHjob']//div[@class='jtag']/div[@class='t1']/span[@class='sp4']")
        if CorporateWelfares:
            item['CorporateWelfare'] = ''
            for CorporateWelfare in CorporateWelfares:
                item['CorporateWelfare'] += CorporateWelfare.xpath(".//text()").extract()[0]
                item['CorporateWelfare'] += ' | '
        else:
            item['CorporateWelfare'] = None


        tBorderTop_box = response.xpath("//div[@class='tCompany_main']/div[@class='tBorderTop_box']")
        JobInformations = tBorderTop_box[0].xpath(".//div[@class='bmsg job_msg inbox']/p|.//div[@class='bmsg job_msg inbox']/div")
        item['JobInformation'] = ''
        for JobInformation in JobInformations:
            JobInfo = JobInformation.xpath(".//text()").extract()
            if JobInfo:
                item['JobInformation'] += JobInfo[0]
                item['JobInformation'] += '<br/>'
            else:
                continue


        FunctionalCategorieses = tBorderTop_box[0].xpath(".//div[@class='bmsg job_msg inbox']/div[@class='mt10']/p[1]/a")
        if FunctionalCategorieses:
            item['FunctionalCategories'] = ''
            for FunctionalCategories in FunctionalCategorieses:
                item['FunctionalCategories'] += FunctionalCategories.xpath(".//text()").extract()[0]
                item['FunctionalCategories'] += '|'
        else:
            item['FunctionalCategories'] = None
        
        Keywords = tBorderTop_box[0].xpath(".//div[@class='bmsg job_msg inbox']/div[@class='mt10']/p[2]/a")
        if Keywords:
            item['Keyword'] = ''
            for Keyword in Keywords:
                item['Keyword'] += Keyword.xpath(".//text()").extract()[0]
                item['Keyword'] += '|'
        else:
            item['Keyword'] = None

        item['CompanyInformation'] = tBorderTop_box[2].xpath(".//div[@class='tmsg inbox']/text()").extract()[0]
        return item  