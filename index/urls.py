# -*- encoding: utf-8 -*-
from django.urls import path
from .views import index, change_password


urlpatterns = [
    path("", index, name='index'),
    path("change_password", change_password, name='change_password'),

]
