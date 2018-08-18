# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector

class PhpSpider(scrapy.Spider):
    name = 'php'
    allowed_domains = ['php.net']
    start_urls = ['http://php.net/manual/zh/'] #开始页面

    #爬取过的页面
    crawled_pages = {}

    #记录爬取的页面
    output_file = 'crawled_php_pages.csv'

    def parse(self, response):

        selector = Selector(response)

        func_list = selector.xpath('//li/a')
        for func in func_list:
            new_page = func.xpath('@href').extract_first()
            #new_page_url = response.urljoin(new_page)
            #print new_page_url

            if new_page is not None:
                if self.crawled_pages.get(new_page) is None:

                    new_page_url = response.urljoin(new_page)

                    yield scrapy.Request(url=new_page_url, callback=self.parse)
                    #crawled page record
                    self.crawled_pages[new_page] = 1;

                    #write file
                    with open(self.output_file, 'a') as f:
                        f.write(new_page_url+'\n')
            