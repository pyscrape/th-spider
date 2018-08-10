# -*- coding: utf-8 -*-
import scrapy
from .. import items


class CnetSpider(scrapy.Spider):
    name = 'cnet'
    allowed_domains = ['cnet.com']
    start_urls = ['https://www.cnet.com/news/']

    def parse(self, response):
        yield scrapy.Request(response.url, callback=self.parse_index)
        next_page_url = response.xpath(
            '//a[@class="load-more"]/@href').extract_first()
        if next_page_url:
            next_page_url = response.urljoin(next_page_url)
            yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_index(self, response):
        latest_news_tags = response.xpath('//div[@class="col-5 assetText"]')

        for news_tag in latest_news_tags:
            yield scrapy.Request(response.urljoin(news_tag.xpath('h3/a/@href').extract_first()), callback=self.parse_article)

    def parse_article(self, response):
        article_head_tag = response.xpath('//div[@class="col-10 articleHead"]')
        news = items.CnetItem()
        news['title'] = article_head_tag.xpath('h1/text()').extract_first()
        news['summary'] = article_head_tag.xpath('p/text()').extract_first()
        news['author'] = article_head_tag.xpath(
            '//a[@rel="author"]/span/text()').extract_first()

        content = []
        content_tag = response.xpath(
            '//div[@class="col-7 article-main-body row"]/node()')
        for tag in content_tag:
            name = tag.xpath('name()').extract_first()
            if name == 'p':
                content.append(tag.extract())
        news['content'] = content
        yield news
