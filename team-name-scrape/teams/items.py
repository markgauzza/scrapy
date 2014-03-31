# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class TeamsItem(Item):
    # define the fields for your item here like:
    name = Field()
    sport = Field()
    firstLetter = Field()
    pass

class LetterItem(Item):
    firstLetter = Field()
    count = Field()
    names = Field()
    pass