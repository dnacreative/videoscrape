# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field
    
class VideoItem(Item):
    url = Field()
    artist = Field()
    title = Field()
    image = Field()
    embed_url = Field()
    