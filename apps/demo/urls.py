# -*- encoding: utf-8 -*-
from django.urls import path, re_path
from apps.demo import views

urlpatterns = [

    # The demo page
    path('', views.index, name='demo'),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
