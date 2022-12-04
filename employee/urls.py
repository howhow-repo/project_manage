# -*- encoding: utf-8 -*-
from django.urls import path
from .views import view_all_users, register_user, edit_user, delete_user

urlpatterns = [
    path("", view_all_users, name='view_all_users'),
    path("register_user", register_user, name='register_user'),
    path("edit_user/<str:username>", edit_user, name='edit_user'),
    path("delete_user/<str:username>", delete_user, name='delete_user'),
]
