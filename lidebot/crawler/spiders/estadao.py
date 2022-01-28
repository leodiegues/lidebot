import scrapy
from datetime import datetime

from crawler.items import Headline


class EstadaoSpider(scrapy.Spider):
    name = "estadao"
    allowed_domains = ["estadao.com.br"]
    start_urls = ["http://estadao.com.br/"]

    def parse(self, response):
        headline_tag = response.css("div.intro")[0].css("a:nth-of-type(1)")
        print(headline_tag)
        yield Headline(
            title=headline_tag.css("::attr(title)")[0].extract(),
            url=headline_tag.css("::attr(href)")[0].extract(),
            collected_at=datetime.now(),
            source=self.name,
        )
