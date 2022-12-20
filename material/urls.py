from django.urls import path
from .views import list_materials, add_material, material_detail

urlpatterns = [
    path("", list_materials, name='list_materials'),
    path("add", add_material, name='add_material'),
    path("<str:material_name>", material_detail, name='material_detail'),

]
