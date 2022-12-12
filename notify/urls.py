from django.urls import path
from .views import add_schedule_notify


urlpatterns = [
    path("add", add_schedule_notify, name='add_schedule_notify'),
]
