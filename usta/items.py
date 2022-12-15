# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class UstaMatchItem(scrapy.Item):
    # define the fields for your item here like:
    eventName = scrapy.Field()
    roundName = scrapy.Field()
    winner1 = scrapy.Field()
    winner2 = scrapy.Field()
    loser1 = scrapy.Field()
    loser2 = scrapy.Field()

    pass
