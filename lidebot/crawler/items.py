# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Headline(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    collected_at = scrapy.Field()
    source = scrapy.Field()
