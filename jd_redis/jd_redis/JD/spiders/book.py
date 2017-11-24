# -*- coding: utf-8 -*-
import scrapy
from JD.items import JdItem
import json
from scrapy_redis.spiders import RedisSpider


class BookSpider(RedisSpider):
    name = 'book'
    # allowed_domains = ['jd.com','3.cn']
    # 修改起始的url
    # start_urls = ['https://book.jd.com/booksort.html']

    def __init__(self,*args,**kwargs):
        domain = kwargs.pop('domain','')
        self.allowed_domans = list(filter(None,domain.split(',')))
        super(BookSpider,self).__init__(*args,**kwargs)

    redis_key = 'python3'




    def parse(self, response):
        # 获取所有大分类列表
        big_cate_list = response.xpath('//*[@id="booksort"]/div[2]/dl/dt')
        print (len(big_cate_list))
        # 遍历大分类列表
        for big_cate in big_cate_list[0:1]:
            temp = {}
            temp['big_cate'] = big_cate.xpath('./a/text()').extract_first()
            temp['big_cate_link'] = 'https:' + big_cate.xpath('./a/@href').extract_first()

            # 小分类列表
            node_list = big_cate.xpath('./following-sibling::dd[1]/em/a')
            for node in node_list[0:1]:
                temp['small_cate'] = node.xpath('./text()').extract_first()
                temp['small_cate_link'] = 'https:' +  node.xpath('./@href').extract_first()

                # 发起书记页面的请求
                yield scrapy.Request(
                    temp['small_cate_link'],
                    callback=self.parse_book_list,
                    meta={'meta_1':temp}
                )


    def parse_book_list(self, response):
        temp = response.meta['meta_1']
        # print ('----',temp)

        # 获取书籍节点列表
        book_list = response.xpath('//*[@id="plist"]/ul/li/div')
        # print (len(book_list))
        # 遍历
        for book in book_list:
            item = JdItem()

            # 提取图书信息
            item['big_cate'] = temp['big_cate']
            item['big_cate_link'] = temp['big_cate_link']
            item['small_cate'] = temp['small_cate']
            item['small_cate_link'] = temp['small_cate_link']

            item['book_name'] = book.xpath('./div[3]/a/em/text()').extract_first()
            if item['book_name'] != None:
                item['book_name'] = item['book_name'].strip()
            item['cover_link'] = book.xpath('./div[1]/a/img/@src|./div[1]/a/img/@data-lazy-img').extract_first()

            item['detail_url'] = book.xpath('./div[1]/a/@href').extract_first()
            if item['detail_url'] != None:
                item['detail_url'] = 'https:' + item['detail_url']

            item['authors'] = book.xpath('./div[4]/span[1]/span/a/text()').extract()
            item['publisher'] = book.xpath('./div[4]/span[2]/a/text()').extract_first()

            item['pub_time'] = book.xpath('./div[4]/span[3]/text()').extract_first()
            if item['pub_time'] != None:
                item['pub_time'] = item['pub_time'].strip()

            item['sku'] = book.xpath('./@data-sku').extract_first()
            # print (item)

            # 发起价格请求
            if item['sku'] != None:
                url = 'https://p.3.cn/prices/mgets?skuIds=J_' + item['sku']
                yield scrapy.Request(url,callback=self.parse_price,meta={'meta_2':item})


    def parse_price(self, response):
        item = response.meta['meta_2']
        price = json.loads(response.text)[0]['op']
        print ('---',price)
        item['price'] = price
        # print(item)
        yield item