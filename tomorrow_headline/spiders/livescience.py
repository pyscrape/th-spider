# -*- coding: utf-8 -*-
import scrapy
from .. import items

class livescienceSpider(scrapy.Spider):
    name = "livescience"
    start_urls = [
        'https://www.livescience.com/technology',
    ]

    def parse(self, response):
        # follow links to detail page
        for href in response.xpath(
                '//div[@class = "pure-u-3-4 pure-u-md-2-3 pure-u-lg-2-3 list-text"]/h2/a/@href').extract():
            yield response.follow(href, self.parse_detail)
        # follow pagination links
        for href in response.xpath('//link[@rel = "next"]/@href').extract():
            yield response.follow(href, self.parse)

    def parse_detail(self, response):
        news = Item.ArticleItem()
        news['title'] = response.xpath('//h1/text()').extract_first()
        news['author'] = response.xpath('//span[@class = "author"]/text()').extract_first()
        news['image'] = response.xpath(
            '//div[@class = "magnify-wrapper iZoom"]/img[@class = "pure-img "]/@big-src').extract_first()
        news['src'] = 'livescience'

        news['content'] = response.xpath(
            '//div[@class="article-content"]').extract()
        news['url'] = response.url

        '''
        article = []
        article.append()
        for sub_tag in response.xpath('//div[@class="article-content"]/node()'):
            name = sub_tag.xpath('name()').extract_first()
            if name == 'p':
                article.append(sub_tag.xpath(
                    '//p/text()').extract())
            elif name == 'figure':
                print(response.xpath('//img/@src').extract_first())
                article.append(sub_tag.xpath(
                    '//img[@class="pure-img lazy"]/@big-src').extract_first())
            elif name == 'h2':
                article.append(sub_tag.xpath(
                    '//h2/text()').extract_first())
        '''
        yield  news


'''   # follow pagination links
        for href in response.xpath('//link[@rel = "next"]/@href').extract():
            yield response.follow(href, self.parse)   
'''


