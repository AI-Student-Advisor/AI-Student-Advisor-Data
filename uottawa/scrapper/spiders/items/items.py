# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class UottawaCatalogItem(scrapy.Item):
    subject: str = scrapy.Field()
    course_code: str = scrapy.Field()
    course_name: str = scrapy.Field()
    course_units: int = scrapy.Field()
    course_description: str = scrapy.Field()
    course_components: str = scrapy.Field()
    course_prerequisites: str = scrapy.Field()

class VectorStoreItem(scrapy.Item):
    id: str = scrapy.Field()
    text: str = scrapy.Field()
    source: str = scrapy.Field()
    metadata: dict = scrapy.Field()