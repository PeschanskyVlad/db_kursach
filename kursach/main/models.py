# python 3
# -*- coding: utf-8 -*-
from datetime import timedelta, datetime

from mongoengine import *
from mongoengine.queryset.visitor import Q
from datetime import date

from itertools import groupby
from os.path import join

from bson import json_util

class Item(Document):
    title = StringField()
    category = StringField()
    date = DateTimeField()  # this stands for our crawled data
    views = IntField()
    text = StringField()
    link = StringField()


def add_new_item(title, date, views, text, link, category):

        exist = Item.objects(link=link)
        if exist:
            return 0

        item = Item()
        item.title = title
        item.category = category
        item.date = date
        item.views = int(views)
        item.text = text
        item.link = link
        return item.save()


def get_by_string(search):
    return Item.objects(Q(title__icontains=search)|Q(text__icontains=search))


def get_last_week():
    date_N_days_ago = date.today() - timedelta(days=7)
    return Item.objects(Q(date__gte=date_N_days_ago)&Q(date__lte=date.today()))


def get_top_news(day):
    return Item.objects(date=day).order_by("-views")[:5]


def get_list_for_graphic(day):
    return [
        Item.objects(Q(category='auto')&Q(date=day)).sum('views'),
        Item.objects(Q(category='culture')&Q(date=day)).sum('views'),
        Item.objects(Q(category='economics')&Q(date=day)).sum('views'),
        Item.objects(Q(category='health')&Q(date=day)).sum('views'),
        Item.objects(Q(category='incident')&Q(date=day)).sum('views'),
        Item.objects(Q(category='politics')&Q(date=day)).sum('views'),
        Item.objects(Q(category='realty')&Q(date=day)).sum('views'),
        Item.objects(Q(category='reclama')&Q(date=day)).sum('views'),
        Item.objects(Q(category='science')&Q(date=day)).sum('views'),
        Item.objects(Q(category='social')&Q(date=day)).sum('views'),
        Item.objects(Q(category='sport')&Q(date=day)).sum('views'),
        Item.objects(Q(category='tech')&Q(date=day)).sum('views'),
        Item.objects(Q(category='woman')&Q(date=day)).sum('views')
    ]


def get_by_day(day):
    return Item.objects(date=day)


def get_all():
    return Item.objects()


def dump_db():
    with open("D:/Labs/Petrashenko/2semestr/kursach/kursach/kursach/data/items.json", 'w') as jsonfile:
        jsonfile.write(Item.objects().to_json())




def loads(self, data):
    return json_util.loads(data.decode('utf-8'))