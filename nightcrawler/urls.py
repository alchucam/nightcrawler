# coding: utf-8

from django.contrib import admin
from django.urls import path, include
from nightcrawler.apps.services import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/statuscheck/', include('celerybeat_status.urls')),
    path('', views.home, name="home"),
    path('news_front/', views.news_front, name="news_front"),
    path('news_front/<publisher>/', include(('nightcrawler.apps.services.urls', 'index'), namespace="news")),
    path('analysis/', views.analysis, name="analysis"),
]
