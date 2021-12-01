import scrapy
from datetime import datetime

from crawler.items import Headline


class EstadaoSpider(scrapy.Spider):
    name = "estadao"
    allowed_domains = ["estadao.com.br"]
    start_urls = ["http://estadao.com.br/"]

    def parse(self, response):
        headline_tag = response.css("div.intro:nth-of-type(1) > a")
        yield Headline(
            title=headline_tag.css("::text").extract(),
            url=headline_tag.css("::attr(href)").extract(),
            collected_at=datetime.now(),
            source=self.name,
        )
