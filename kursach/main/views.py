from django.shortcuts import render
from uuid import uuid4
from urllib.parse import urlparse
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.views.decorators.http import require_POST, require_http_methods

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from scrapyd_api import ScrapydAPI
import plotly
import plotly.graph_objs as go
from datetime import timedelta, datetime
from dateutil import parser

from mongoengine import *

from datetime import date

from main.models import *

#get_last_week()



# connect scrapyd service
scrapyd = ScrapydAPI('http://localhost:6800')


def dump(request):
    dump_db()
    return redirect("/")



def all(request):
    all = get_all()

    search = "none"
    is_search = False
    is_empty = True

    if request.method == "POST":
        _search = request.POST['search']

        all = get_by_string(_search)
        if all:
            is_empty = False
        is_search = True
        search = _search

    return render(request, 'all.html', locals())


def handle_day(request, id):
    str = id.replace("S", " ")
    _day = parser.parse(str)

    list_for = get_list_for_graphic(_day)
    trace1 = go.Bar(
        x=['авто', 'культура', 'экономика', 'медицина', 'проишествия', 'политика', 'жизнь', 'реклама', 'наука',
           'социиум', 'спорт', 'техника', 'отношения'],
        y=list_for,
        name='categories'
    )
    data = [trace1]
    layout = go.Layout(
        barmode='group'
    )
    fig = go.Figure(data=data, layout=layout)
    div = plotly.offline.plot(fig, show_link=False, auto_open=False, output_type='div')

    day = get_by_day(_day)
    top = get_top_news(_day)

    return render(request, 'index.html', locals())


def home(request):
    list_for = get_list_for_graphic(date.today())
    trace1 = go.Bar(
        x=['авто', 'культура', 'экономика', 'медицина', 'проишествия', 'политика', 'жизнь', 'реклама', 'наука', 'социиум', 'спорт', 'техника', 'отношения'],
        y=list_for,
        name='categories'
    )
    data = [trace1]
    layout = go.Layout(
        barmode='group'
    )
    fig = go.Figure(data=data, layout=layout)
    div = plotly.offline.plot(fig, show_link=False, auto_open=False, output_type='div')

    day = get_by_day(date.today())
    top = get_top_news(date.today())


    return render(request, 'index.html', locals())


def is_valid_url(url):
    validate = URLValidator()
    try:
        validate(url)  # check if url format is valid
    except ValidationError:
        return False

    return True


@csrf_exempt
@require_http_methods(['POST', 'GET'])  # only get and post
def crawl(request):
    # Post requests are for new crawling tasks
    if request.method == 'POST':
        target = request.POST.get('target', None)  # take url comes from client. (From an input may be?)

        if target == "korr":
            url = "https://korrespondent.net/"
            domain = urlparse(url).netloc  # parse the url and extract the domain
            settings = {

                'USER_AGENT': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
            }

            task = scrapyd.schedule('default', 'korrspider',
                                    settings=settings)

            print("Domain = " + domain  + " TASK_ID = " + task)

            return JsonResponse({'task_id': task, 'status': 'started'})

        if target == "ukra":
            url = "https://ukranews.com/"
            domain = urlparse(url).netloc  # parse the url and extract the domain


            settings = {
                'USER_AGENT': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
            }

            task = scrapyd.schedule('default', 'ukranewsspider',
                                    settings=settings)

            print("Domain = " + domain + " TASK_ID = " + task)

            return JsonResponse({'task_id': task, 'status': 'started'})

    elif request.method == 'GET':
        task_id = request.GET.get('task_id', None)

        if not task_id:
            return JsonResponse({'error': 'Missing args'})

        status = scrapyd.job_status('default', task_id)

        if status == 'finished':

            try:
                return JsonResponse({'data': "Success"})
            except Exception as e:
                return JsonResponse({'error': str(e)})
        else:

            return JsonResponse({'status': status})