# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector

class HanyuSpider(scrapy.Spider):
    name = 'hanyu'
    allowed_domains = ['hanyu.baidu.com']
    start_urls = [
        'https://hanyu.baidu.com/s?wd=%E5%A4%A9&ptype=zici',
        #'https://hanyu.baidu.com/s?wd=%E5%9C%B0&from=zici',
        #'https://hanyu.baidu.com/s?wd=%E4%BA%BA&from=zici'
    ]
    crawled_pages = {}

    output_file = 'crawled_pages.csv'

    def parse(self, response):

        selector = Selector(response)

        zici_list = selector.xpath('//li[@class="recmd-item recmd-item-grid"]/a[@class="text-link"]')
        for zici in zici_list:
            new_page = zici.xpath('@href').extract_first()

            if new_page is not None:
                if self.crawled_pages.get(new_page) is None:
            	    new_page_url = response.urljoin(new_page)

                    yield scrapy.Request(url=new_page_url, callback=self.parse)
                    #crawled page record
                    self.crawled_pages[new_page] = 1;

                    #write file
                    with open(self.output_file, 'a') as f:
                        f.write(new_page_url+'\n')

