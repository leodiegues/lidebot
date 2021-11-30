from datetime import datetime
import scrapy

from crawler.items import Headline


class ValorSpider(scrapy.Spider):
    name = "valor"
    allowed_domains = ["valor.com.br"]
    start_urls = ["http://valor.com.br/"]

    def parse(self, response):
        headline_tag = response.css("a.bstn-dedupe-url")[0]
        yield Headline(
            title=headline_tag.css("::attr(title)").extract_first(),
            url=headline_tag.css("::attr(href)").extract_first(),
            collected_at=datetime.now(),
            source=self.name,
        )
