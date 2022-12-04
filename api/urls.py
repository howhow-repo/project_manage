# -*- encoding: utf-8 -*-
from django.urls import path
from api.views import CheckServerHealth, Login, Logout, AmILogin


urlpatterns = [
    path('CheckServerHealth', CheckServerHealth.as_view(), name='CheckServerHealth'),
    path('User/Login', Login.as_view(), name='api_login'),
    path('User/Logout', Logout.as_view(), name='api_logout'),
    path('User/AmILogin', AmILogin.as_view(), name='AmILogin'),
]
