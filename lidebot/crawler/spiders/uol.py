from datetime import datetime
import scrapy

from crawler.items import Headline


class UolSpider(scrapy.Spider):
    name = "uol"
    allowed_domains = ["uol.com.br"]
    start_urls = ["http://uol.com.br/"]

    def parse(self, response):
        headline_tag = response.css("a.headlineMain__link")
        yield Headline(
            title=headline_tag.css(
                "div > h3.headlineMain__title::text"
            ).extract_first().strip(),
            url=headline_tag.css("::attr(href)").extract_first(),
            collected_at=datetime.now(),
            source=self.name,
        )
