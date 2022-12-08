from django.urls import path
from .views import list_materials

urlpatterns = [
    path("", list_materials, name='list_materials'),

]
