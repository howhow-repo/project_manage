from django.urls import path
from .views import add_bom

urlpatterns = [
    path("add/<str:project_id>", add_bom, name='add_bom'),
]
