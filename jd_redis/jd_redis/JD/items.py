# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JdItem(scrapy.Item):
    # define the fields for your item here like:
    # 书名
    book_name = scrapy.Field()
    # 大分类
    big_cate = scrapy.Field()
    # 大分类链接
    big_cate_link = scrapy.Field()
    # 小分类
    small_cate = scrapy.Field()
    # 小分类链接
    small_cate_link = scrapy.Field()
    # 封面链接
    cover_link = scrapy.Field()
    # 详情url
    detail_url = scrapy.Field()
    # 作者
    authors = scrapy.Field()
    # 出版商
    publisher = scrapy.Field()
    # 出版时间
    pub_time = scrapy.Field()
    # 图书价格
    price = scrapy.Field()
    sku = scrapy.Field()
