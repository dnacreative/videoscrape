# -*- coding: utf-8 -*-
'''
Created on Dec 30, 2011

@author: paul
'''
from videoscrape.pipelines import SeleniumScraperPipeline
from videoscrape.items import VideoItem
from videoscrape.pipelines import FlaskPipeline

import unittest

class PitchforkTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.scraper = SeleniumScraperPipeline()

    @classmethod
    def tearDownClass(cls):
        cls.scraper.spider_closed(None)
    
    def setUp(self):
        pass

    def tearDown(self):
        pass
        
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

    def test_pitchfork_1979_bashful(self):
        url ="http://pitchfork.com/tv/musicvideos/1979-bashful/"
        self._assert_video(url,'http://www.youtube.com/embed/z9llB97Qj_8?fs=1&feature=oembed')

    def test_pitchfork_1978_oj(self):
        url = "http://pitchfork.com/tv/musicvideos/1978-oj/"
        self._assert_video(url,'http://player.vimeo.com/video/40512220')
        
    def test_pitchfork_2079_baby(self):
        url = "http://pitchfork.com/tv/musicvideos/2079-baby/"
        self._assert_video(url,'http://www.youtube.com/embed/ZJJfXI96J6k?fs=1&feature=oembed')
        
    def test_pitchfork_2051_grown_up(self):        
        url = "http://pitchfork.com/tv/musicvideos/2051-grown-up/"
        self._assert_video(url,'http://www.youtube.com/embed/NHfWY0is3rE?fs=1&feature=oembed')
        
    def _assert_video(self, vurl, expected_src):
        result = self.scraper.parse_detail_with_selenium(vurl)
        self.assertEqual(expected_src, result)


class PipelineTests(unittest.TestCase):
    
    def test_flask_pipeline(self):
        
        item = VideoItem()
        item["embed_url"] = "http://player.vimeo.com/video/41088675"
        item["artist"] = "Mirel Wagner"
        item["url"] = "http://pitchfork.com/tv/musicvideos/1983-joe/"
        item["image"] = "http://cdn3.pitchfork.com/video-archive/1983/medium.bb8aa5ef.jpg"
        item["title"] = "Joe"
        
        pipeline = FlaskPipeline()
        result = pipeline.process_item(item, None)
        self.assertIsNotNone(result, "No result from pipeline.")

        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_pitchfork_selenium']
    unittest.main()