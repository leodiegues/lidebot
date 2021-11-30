import scrapy


class OgloboSpider(scrapy.Spider):
    name = 'oglobo'
    allowed_domains = ['oglobo.com.br']
    start_urls = ['http://oglobo.com.br/']

    def parse(self, response):
        pass
