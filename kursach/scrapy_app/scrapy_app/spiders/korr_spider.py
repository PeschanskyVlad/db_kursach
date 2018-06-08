# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_app.util import parse_date
from datetime import datetime, timedelta


def scrap_links_page(request):
    for link in request.css('.article > a::attr(href)'):
        yield request.follow(link.extract(), callback=scrap_page)


def scrap_page(request):
    title = request.css('h1.post-item__title::text').extract_first()

    time = request.css('.post-item__info::text').extract_first()

    views = request.css('.post-item__views > span::text').extract_first()
    text = request.css('.post-item__text > h2::text').extract_first()
    link = request.url
    yield {'title': title, 'time': parse_date(time.split(",")[1].strip()), 'views':views, 'text': text.strip(), 'link': link}


class KorrSpider(scrapy.Spider):
    name = 'korrspider'
    now = datetime.now()
    URL = "https://korrespondent.net/all/"+str(now.year)+"/"+now.strftime("%B").lower()+"/"+str(now.day)+"/"
    print(URL)
    start_urls = [URL]

    custom_settings = {
        'ITEM_PIPELINES': {
            'scrapy_app.pipelines.Pipeline': 400
        }
    }

    def parse(self, response):
        for link in response.css('.article > a::attr(href)'):
            yield response.follow(link.extract(), callback=scrap_page)

        for link in response.css('a.pagination__link::attr(href)'):
            yield response.follow(link.extract(), callback=scrap_links_page)


