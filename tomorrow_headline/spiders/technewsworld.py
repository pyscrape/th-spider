import scrapy
from ..items import ArticleItem

class technewsworld(scrapy.Spider):
    name = 'technewsworld'
    start_urls = [
        'https://www.technewsworld.com/',
    ]

    def parse(self, response):
        # follow links to detail page
        for href in response.xpath(
                '//div[@class = "title"]/a/@href').extract():
            yield response.follow(href, self.parse_detail)
        # follow pagination links
        for href in response.xpath('//div[@id = "earlier"]/a/@href').extract():
            yield response.follow(href, self.parse)

    def parse_detail(self, response):
        news = ArticleItem()
        news['title'] = response.xpath('//h1[@class = "title"]/text()').extract_first()
        author = response.xpath('//div[@id = "story-byline"]/text()').extract()[1]
        news['author'] = author[3: ]
        news['image'] = response.xpath(
            '//div[@id = "story-graphic-xlarge"]/img/@src').extract_first()
        news['src'] = 'technewsworld'

        news['content'] = response.xpath(
            '//div[@id= "story-body"]').extract()
        news['url'] = response.url

        '''article = []
        for sub_tag in response.xpath('//div[@id= "story-body"]/node()'):
            name = sub_tag.xpath('name()').extract_first()
            if name == 'p':
                article.append(sub_tag.xpath(
                    '//p/text()').extract())
                if sub_tag.xpath('//p/hr/div/a/img/@src').extract_first() is True:
                    article.append(sub_tag.xpath(
                    '//p/hr/div/a/img/@src').extract_first())
                if sub_tag.xpath('//p/a/text()') is True:
                    article.append(sub_tag.xpath(
                        '//p/a/text()').extract())
            elif name == 'div':
                #print(response.xpath('//img/@src').extract_first())
                article.append(sub_tag.xpath(
                    '//div[@class = "story-thumbnail"]//img/@src'|'//div[@class = "story-thumbnail"]/a/img/@src').extract())
            elif name == 'h2':
                article.append(sub_tag.xpath(
        '//h2/text()').extract_first())'''
        yield news

