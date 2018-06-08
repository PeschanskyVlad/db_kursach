# python 3
# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urlparse
from scrapy_app.util import parse_date


def scrap_page(request):
    title = request.css('h1.article_title::text').extract_first()
    data = request.css('.article_date::text').extract()
    text = request.css('.article_content > h2.anotation::text').extract_first()
    link = request.url
    yield {'title': title, 'time': parse_date(data[0].split(",")[0]), 'views': data[1], 'text': text.strip(), 'link': link}


class UkranewsSpider(scrapy.Spider):
    name = 'ukranewsspider'
    start_urls = ['https://ukranews.com/archiv/tab/news/']

    custom_settings = {
        'ITEM_PIPELINES': {
            'scrapy_app.pipelines.Pipeline': 400
        }
    }


    def parse(self, response):

        page_num = response.meta.get('page_num')
        if page_num is None:
            page_num = 0

        domain = urlparse(response.url).netloc
        next_url = response.css('.arrow:last-child > a::attr(href)').extract_first()
        result = "https://" + domain + next_url
        print(result)
        req = scrapy.Request(url=result)
        req.meta['page_num'] = page_num + 1
        yield req

        for link in response.css('a.tape_news__item::attr(href)'):
            yield response.follow(link.extract(), callback=scrap_page)