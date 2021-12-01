import scrapy
from datetime import datetime

from crawler.items import Headline


class G1Spider(scrapy.Spider):
    name = "g1"
    allowed_domains = ["g1.com.br"]
    start_urls = ["http://g1.com.br/"]

    def parse(self, response):
        yield Headline(
            title=response.css("span.bstn-hl-title::text").extract_first(),
            url=None,
            collected_at=datetime.now(),
            source=self.name,
        )
