# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from main.models import *
import json
from scrapy_app.settings import MAGIC


class Pipeline(object):
    def __init__(self, *args, **kwargs):
        self.items = []

    def close_spider(self, spider):
        print("Spider finished")

    def process_item(self, item, spider):
        text_for_magic = item['title']+" "+ item['text']
        category = MAGIC.behold_category_name(text_for_magic)

        add_new_item(item['title'], item['time'], item['views'], item['text'], item['link'], category)
                        #  MAGIC.behold_category_name(text_for_magic))
