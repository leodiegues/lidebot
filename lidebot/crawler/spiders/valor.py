import scrapy


class ValorSpider(scrapy.Spider):
    name = 'valor'
    allowed_domains = ['valor.com.br']
    start_urls = ['http://valor.com.br/']

    def parse(self, response):
        pass
