# coding:utf-8
# 链家二手房信息爬虫
import sys
import scrapy

from scrapy import Request
from scrapy import Selector

reload(sys)
sys.setdefaultencoding('utf-8')

class LianjiaSpider(scrapy.Spider):
    name = 'lianjia'

    # 主页：链家深圳二手房首页
    host = 'https://sz.lianjia.com/ershoufang/'

    # 准备爬取的初始页面
    start_urls = ['https://sz.lianjia.com/ershoufang/']

    # 入口解析函数，解析初始页面的内容
    def start_requests(self):
        for url in self.start_urls:
            # 将url加入爬取队列，并指定解析函数，scrapy会自动进行调度
            yield Request(url = url,callback = self.parse_page)
			# sys.exit()

    # 从上一步返回的页面内容中解析单个页面，解析出房子信息列表
    def parse_page(self,resp):
        # 创建Selector对象
        selector = Selector(resp)

        # 房子信息列表
        house_info_list = selector.xpath('//li[@class="clear LOGCLICKDATA"]')

        for info in house_info_list:
            # 标题
            house_title = info.xpath('.//div[@class="title"]/a[re:test(@href, "https://sz\.lianjia\.com/ershoufang/\d+\.html$")]/text()').extract_first()
            print house_title

            # 房屋详细信息，这里用'string(.)'解析出多个不同标签的文本内容
            house_detail = info.xpath('.//div[@class="houseInfo"]').xpath('string(.)').extract_first()
            print house_detail
