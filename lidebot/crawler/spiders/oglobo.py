from datetime import datetime
import scrapy

from crawler.items import Headline


class OgloboSpider(scrapy.Spider):
    name = "oglobo"
    allowed_domains = ["oglobo.com.br"]
    start_urls = ["http://oglobo.com.br/"]

    def parse(self, response):
        headline_tag = response.css("h1.headline__title > a")
        yield Headline(
            title=headline_tag.css("::text").extract_first(),
            url=headline_tag.css("::attr(href)").extract_first(),
            collected_at=datetime.now(),
            source=self.name,
        )
