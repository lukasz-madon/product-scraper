# Define here the models for your scraped items
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field


class OxygenProduct(Item):

    """represents a scraped product"""
    code = Field()
    description = Field()
    designer = Field()
    price = Field()
    gender = Field()
    image_urls = Field()
    name = Field()
    raw_color = Field()
    sale_discount = Field()
    source_url = Field()
    stock_status = Field()
    last_updated = Field()
    type = Field()
