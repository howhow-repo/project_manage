from django.urls import path
from .views import list_options, edit_choices

urlpatterns = [
    path("", list_options, name='list_options'),
    path("<str:option_name>", edit_choices, name='edit_choices'),
]
