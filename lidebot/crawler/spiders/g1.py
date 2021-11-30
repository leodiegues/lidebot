import scrapy


class G1Spider(scrapy.Spider):
    name = 'g1'
    allowed_domains = ['g1.com.br']
    start_urls = ['http://g1.com.br/']

    def parse(self, response):
        pass
