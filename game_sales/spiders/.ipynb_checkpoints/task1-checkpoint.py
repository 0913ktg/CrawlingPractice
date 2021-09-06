import scrapy
import time
from selenium import webdriver
from ..items import GameSalesItem


class Task1Spider(scrapy.Spider):
    name = 'task1'

    kr_market = 'http://www.mobileindex.com/mi-chart/top-charts/chart-by-market'
    global_market = 'http://www.mobileindex.com/mi-chart/top-charts/global-chart-by-market'

    items = GameSalesItem()
    
    def start_requests(self):

        urls = [
            self.kr_market,
            self.global_market
        ]

        meta_list = [
            ['.active+ .visible'],
            ['.disabled-border~ .option+ .option .small label',
             '.false:nth-child(3)']
        ]

        parse_list = [
            self.parse_g,
            self.parse_a
        ]
        for url, parse, meta in zip(urls, parse_list, meta_list):            
            yield scrapy.Request(url = url, 
                                callback = parse, 
                                meta = {'selector' : meta})
            time.sleep(5)
            
            

    
    def parse_g(self, response):
        titles = response.css(".left~ .left+ .left .app span:nth-child(1)::text")
        for title in titles:

            rank = 1
            title = str(title)
            index = title.find('data')
            title = title[index+6:-2]

            self.items['title'] = title
            self.items['country'] = 'korea'
            self.items['market'] = 'google play store'
            rank += 1

            yield self.items
        

    def parse_a(self, response):
        titles = response.css(".left~ .left+ .left .app span:nth-child(1)::text")
        for title in titles:

            title = str(title)
            index = title.find('data')
            title = title[index+6:-2]

            self.items['title'] = title
            self.items['country'] = 'china'
            self.items['market'] = 'app store'

            yield self.items   