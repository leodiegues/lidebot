import scrapy


class UolSpider(scrapy.Spider):
    name = 'uol'
    allowed_domains = ['uol.com.br']
    start_urls = ['http://uol.com.br/']

    def parse(self, response):
        pass
