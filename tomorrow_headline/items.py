# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ArticleItem(scrapy.Item):
    title = scrapy.Field()
    author = scrapy.Field()
    url = scrapy.Field()
    src = scrapy.Field()
    image = scrapy.Field()
    summary = scrapy.Field()
    content = scrapy.Field()
