# -*- coding: utf-8 -*-
from django import template
from django.utils import timezone
from django.urls import reverse

register = template.Library()

@register.simple_tag
def menu_get_url(publisher, delta):
    today = timezone.now()
    date = today - timezone.timedelta(delta)
    return reverse('news:day', args=(publisher, date.year, str(date.month).zfill(2), str(date.day).zfill(2),))

@register.simple_tag
def menu_get_date(delta):
    today = timezone.now()
    date = today - timezone.timedelta(delta)
    return date.strftime('%A').lower()
