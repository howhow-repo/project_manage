# -*- encoding: utf-8 -*-
from django.urls import path, include
from .views import get_daily_report_photo, get_material_cover

urlpatterns = [
    path("daily_report/<str:report_id>/<int:photo_num>", get_daily_report_photo, name='get_daily_report_photo'),
    path("material/<int:material_id>", get_material_cover, name='get_material_cover'),
]
