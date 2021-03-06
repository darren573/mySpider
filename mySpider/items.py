# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class MyspiderItem(Item):
    name = Field()
    title = Field()
    info = Field()


class BookItem(Item):
    name = Field()
    price = Field()
