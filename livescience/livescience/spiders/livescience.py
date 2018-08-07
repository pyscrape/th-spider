import scrapy

from ..items import LivescienceItem


class LivescienceSpider(scrapy.Spider):
    name = 'livescience'
    start_urls = ['https://www.livescience.com/63260-crispr-safety.html']

    def parse(self, response):
        article = []
        for sub_tag in response.xpath('//div[@class="article-content"]/node()'):
            name = sub_tag.xpath('name()').extract_first()
            if name == 'p':
                article.append(sub_tag.xpath(
                    '//p/text()').extract_first())
            elif name == 'figure':
                print(response.xpath('//img/@src').extract_first())
                article.append(sub_tag.xpath(
                    '//img[@class="pure-img lazy"]/@big-src').extract_first())
            elif name == 'h2':
                article.append(sub_tag.xpath(
                    '//h2/text()').extract_first())
        print(article)
