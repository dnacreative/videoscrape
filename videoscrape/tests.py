# -*- coding: utf-8 -*-
'''
Created on Dec 30, 2011

@author: paul
'''
from selenium import webdriver
from videoscrape.spiders.pitchfork import parse_detail_with_selenium
import unittest

class PitchforkTests(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def tearDown(self):
        self.driver.quit()
        
    def test_pitchfork_vimeo(self):
        vimeo_vid_url = 'http://pitchfork.com/tv/musicvideos/1513-possession'
        self._assert_video(vimeo_vid_url,'http://player.vimeo.com/video/30273829?title=0&byline=0&portrait=0')

    def test_pitchfork_youtube(self):
        youtube_vid_url = 'http://pitchfork.com/tv/musicvideos/1606-benefits/'
        self._assert_video(youtube_vid_url,'http://www.youtube.com/v/vjhX6h5Httk?version=3&feature=oembed')

    def test_youtube_iframe(self):
        iframe_vid = 'http://pitchfork.com/tv/musicvideos/1707-motivate-to-be-rich-ft-dallas-tha-kid/'
        self._assert_video(iframe_vid,'http://www.youtube.com/embed/5nCxdYgkFCE?fs=1&feature=oembed')
    
    def test_youtube_iframe2(self):
        p4k = 'http://pitchfork.com/tv/musicvideos/1841-love-is-the-drug-todd-terje-disco-dub/'
        self._assert_video(p4k,'http://www.youtube.com/embed/Ic4xAuIkoFE?fs=1&feature=oembed')

    def _assert_video(self, vurl, expected_src):
        result = parse_detail_with_selenium(self.driver, vurl)
        self.assertEqual(expected_src, result)

#class XPathTests(unittest.TestCase): 
#       
#    def test_vimeo_iframe_xpath(self):
#        """Test vimeo video embeded in iframe."""
#        
#        html = """<iframe width="940" height="519" frameborder="0" allowfullscreen="" webkitallowfullscreen="" src="http://player.vimeo.com/video/30273829?title=0&amp;byline=0&amp;portrait=0"></iframe>"""
#        result = parse_video_with_xpath(html)
#        self.assertTrue("vimeo" in result, "Did not parse iframe video src")
#        
#    def test_youtube_embed_xpath(self):
#        
#        html = """<div class="modal dialog archivevideo open" style="width: 940px; margin-left: -482px; height: 573px; margin-top: -298px;"><div class="embed">
#<object width="940" height="529"><param value="http://www.youtube.com/v/vjhX6h5Httk?version=3&amp;feature=oembed" name="movie"><param value="true" name="allowFullScreen"><param value="always" name="allowscriptaccess"><embed width="940" height="529" allowfullscreen="true" allowscriptaccess="always" type="application/x-shockwave-flash" src="http://www.youtube.com/v/vjhX6h5Httk?version=3&amp;feature=oembed"></object>
#</div></div>"""
#    
#        result = parse_video_with_xpath(html.encode('UTF-8'))
#        self.assertTrue("youtube" in result, "Did not parse youtube embed video src")
        
    
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_pitchfork_selenium']
    unittest.main()