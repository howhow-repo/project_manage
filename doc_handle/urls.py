# -*- encoding: utf-8 -*-
from django.urls import path
from .views import get_daily_report_photo, get_material_cover, get_ticket_photo

urlpatterns = [
    path("daily_report/<str:report_id>/<int:photo_num>", get_daily_report_photo, name='get_daily_report_photo'),
    path("material/<int:material_id>", get_material_cover, name='get_material_cover'),
    path("tickets/<str:ticket_id>/<int:photo_num>", get_ticket_photo, name='get_ticket_photo'),
]
