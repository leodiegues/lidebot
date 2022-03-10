import re
import json
import scrapy
from datetime import datetime

from crawler.items import Headline


class G1Spider(scrapy.Spider):
    name = "g1"
    allowed_domains = ["g1.globo.com"]
    start_urls = ["https://g1.globo.com/"]

    def parse(self, response):
        script_tag_data = response.css("#bstn-launcher-bundle::text").extract_first()

        hl_json = json.loads(
            re.search(r"({ ?\"config\".*}),", script_tag_data).group(1)
        )

        hl = hl_json["items"][0]

        yield Headline(
            title=hl["content"]["title"],
            url=hl["content"]["url"],
            collected_at=datetime.now(),
            source=self.name,
        )
