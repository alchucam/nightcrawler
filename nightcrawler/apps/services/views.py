# -*- coding: utf-8 -*-

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from django.shortcuts import render, get_list_or_404
from django.utils import timezone

from nightcrawler.apps.services.updater import *
from nightcrawler.apps.services.displayer import *


def home(request):
    return render(request, 'services/home.html')

def news_front(request):
    queryset = displayer().news_front_displayer()
    today = timezone.now()
    today_time = date(int(today.year), int(today.month), int(today.day))
    return render(request, 'services/news_front.html', {'queryset':queryset, 'today_time':today_time})

def news(request, queryset, subtitle):
    paginator = Paginator(list(queryset), 10) #list/tuple. not other types.
    page = request.GET.get('page')
    try:
        newspage = paginator.get_page(page)
    except PageNotAnInteger:
        newspage = paginator.page(1)
    except EmptyPage:
        newspage = paginator.page(paginator.num_page)
    index = newspage.number - 1
    max_index = len(paginator.page_range)
    start_index = index - 5 if index >= 5 else 0
    end_index = index + 5 if index <= max_index - 5 else max_index
    page_range = list(paginator.page_range)[start_index:end_index]
    return render(request, 'services/news.html', {'newspage':newspage, 'subtitle': subtitle,
    'page_range':page_range})


def index(request, publisher):
    today = timezone.now()
    return day(request, publisher, today.year, today.month, today.day)

def day(request, publisher, year, month, day):
    dates = date(int(year), int(month), int(day))
    try:
        queryset = get_list_or_404(newsData.objects.order_by('-id'), publisher=publisher, date=dates)
    except:
        queryset = {}
    subtitle = {"publisher":publisher, "date":dates}
    return news(request, queryset, subtitle)


def analysis(request):
    data = displayer()
    template_data = data.analysis_displayer()
    ratio_data = data.ratio_displayer()

    return render(request, 'services/analysis.html', {'template_data':template_data, 'ratio_data':ratio_data})

def search(request):
    query = request.GET.get('q')
    results = Post.objects.filter(Q(title__icontains=query))
    return render(request, 'services/analysis.html')
