# -*- encoding: utf-8 -*-
from django.urls import path
from .views import index, change_password
from .views import add_favorite_project, rm_favorite_project, add_favorite_customer, rm_favorite_customer


urlpatterns = [
    path("", index, name='index'),
    path("change_password", change_password, name='change_password'),
    path("add_favorite_project/<str:project_id>", add_favorite_project, name="add_favorite_project"),
    path("rm_favorite_project/<str:project_id>", rm_favorite_project, name="rm_favorite_project"),
    path("add_favorite_customer/<str:customer_id>", add_favorite_customer, name="add_favorite_customer"),
    path("rm_favorite_customer/<str:customer_id>", rm_favorite_customer, name="rm_favorite_customer")

]
