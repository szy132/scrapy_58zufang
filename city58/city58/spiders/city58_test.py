# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector
from ..items import City58Item
import time


class City58TestSpider(scrapy.Spider):
    name = 'city58_test'
    allowed_domains = ['58.com']
    start_urls = ['http://bj.58.com/chuzu/']

    def parse(self, response):
        xp = Selector(response)
        li_list = xp.xpath('/html/body/div[3]/div[1]/div[5]/div[2]/ul/li')
        for it in li_list:
            item = City58Item()
            item['name'] = it.xpath('normalize-space(div[2]/h2/a/text())').extract()
            item['url'] = it.xpath('normalize-space(div[2]/h2/a/@href)').extract()
            item['price'] = it.xpath('normalize-space(div[3]/div[2]/b/text())').extract()

            if item['url']:
                chilrenurl = it.xpath('normalize-space(div[2]/h2/a/@href)').extract()[0]
                # print(chilrenurl)
                yield scrapy.Request(response.urljoin(chilrenurl), callback=self.chilren_parse, meta={'item': item},
                                     dont_filter=True)

        next_url = xp.xpath('//*[@id="bottom_ad_li"]/div[2]/a[@class="next"]/@href').extract_first()
        if next_url:
            print(next_url)
            yield scrapy.Request(response.urljoin(next_url), callback=self.parse, dont_filter=True)

    def chilren_parse(self, response):
        # time.sleep(1)
        xp = Selector(response)
        item = response.meta['item']
        item['roomType'] = xp.xpath(
            'normalize-space(/html/body/div[4]/div[2]/div[2]/div[1]/div[1]/ul/li[2]/span[2]/text())').extract()
        yield item
