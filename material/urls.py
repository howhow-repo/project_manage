from django.urls import path
from .views import list_materials, add_material

urlpatterns = [
    path("", list_materials, name='list_materials'),
    path("add", add_material, name='add_material'),

]
