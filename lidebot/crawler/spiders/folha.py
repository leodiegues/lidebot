import scrapy
from datetime import datetime

from crawler.items import Headline


class FolhaSpider(scrapy.Spider):
    name = "folha"
    allowed_domains = ["folha.uol.com.br"]
    start_urls = ["http://folha.uol.com.br/"]

    def parse(self, response):
        yield Headline(
            title=response.css("h2.c-main-headline__title::text").extract_first(),
            url=response.css("a.c-main-headline__url::attr(href)").extract_first(),
            collected_at=datetime.now(),
            source=self.name,
        )
