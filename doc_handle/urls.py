# -*- encoding: utf-8 -*-
from django.urls import path, include
from .views import get_daily_report_photo

urlpatterns = [
    path("<str:report_id>/<int:photo_num>", get_daily_report_photo, name='get_daily_report_photo'),
]
