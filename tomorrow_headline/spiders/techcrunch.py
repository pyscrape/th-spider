import scrapy
from ..items import ArticleItem

class technewsworld(scrapy.Spider):
    name = 'techcrunch'
    start_urls = [
        'https://techcrunch.com/',
    ]

    def parse(self, response):
        # follow links to detail page
        for href in response.xpath(
                '//footer[@class = "post-block__footer"]/figure/a/@href').extract():
            yield response.follow(href, self.parse_detail)
        # follow pagination links
        for href in response.xpath('//div[@id = "root"]/div/div/div/a/@href').extract():
            yield response.follow(href, self.parse)

    def parse_detail(self, response):
        news = ArticleItem()
        news['title'] = response.xpath('//div[@class = "article__title-wrapper"]/h1/text()').extract_first()
        news['author'] = response.xpath('//div[@class = "article_byline"]/a/text()').extract_first()
        news['image'] = response.xpath(
            '//div[@class = "article__featured-image-wrapper breakout"]/img/@src').extract_first()
        news['src'] = 'techcrunch'

        news['content'] = response.xpath(
            '//div[@class="article-content"]').extract()
        news['url'] = response.url
        '''
        article = []
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
                    '//h2/text()').extract_first())'''

        yield news
