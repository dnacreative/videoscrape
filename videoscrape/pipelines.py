# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

import pymongo

from scrapy.conf import settings
from scrapy import log

from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from scrapy.exceptions import DropItem

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

from flask import Flask
from video.models import Video

class SeleniumScraperPipeline(object):

    def __init__(self):
        # selenium driver
        self.driver = webdriver.Firefox()
        
        dispatcher.connect(self.spider_opened, signals.spider_opened)
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_opened(self, spider):
        pass
    
    def spider_closed(self, spider):
        self.driver.quit()

    def process_item(self, item, spider):
        embed_src = self.parse_detail_with_selenium(item['url'])
        item['embed_url'] = embed_src
        return item
    
    def parse_detail_with_selenium(self, url):
        self.driver.implicitly_wait(10)
        self.driver.get(url)
        embed_src = None
        
        try:
            
            driver = self.driver
            
            #wait until modal video pops up
            modal_dialog_open = '//div[contains(@class,"modal") and contains(@class ,"dialog") and contains(@class ,"open")]'
            WebDriverWait(driver, 10).until(lambda driver : driver.find_element_by_xpath(modal_dialog_open))
            
            # look for iframes first
            iframes = self.driver.find_elements_by_xpath('//iframe')
            if iframes:        
                iframe_src_attrs = [iframe.get_attribute('src') for iframe in iframes]
                print "Found iframe src = %s" % iframe_src_attrs
                for i in iframe_src_attrs:
                    if "vimeo" in i:
                        return i
                    if "youtube" in i:
                        return i
                    
            # look for embed objects     
            embed = self.driver.find_element_by_xpath('//div[@class="embed"]/object/embed')   
            embed_src = embed.get_attribute('src')    
        except Exception as e:
            print e, url
            raise DropItem("Exception processing url: %s" % url)
        
        return embed_src

class FlaskPipeline(object):
    def __init__(self):
        app = Flask(__name__)
        app.config.from_object('video.settings')
        
    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing %s from %s" % (data, item['url']))
                log.msg("Missing %s from %s" % (data, item['url']))
        if valid:
            vid = Video(embed_url=item["embed_url"],
                    artist=item["artist"],
                    url=item["url"],
                    image=item["image"],
                    title=item["title"])
            vid.save()
            print "Saved video %s " % vid
            log.msg("Video saved to database %s" % vid, level=log.DEBUG, spider=spider) 
        return item
