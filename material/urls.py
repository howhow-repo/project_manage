from django.urls import path
from .views import list_materials, add_material, material_detail, material_type, del_material_type

urlpatterns = [
    path("", list_materials, name='list_materials'),
    path("add", add_material, name='add_material'),
    path("material_type", material_type, name='material_type'),
    path("material_type/<str:type_name>/delete", del_material_type, name='del_material_type'),
    path("<str:material_name>", material_detail, name='material_detail'),

]
