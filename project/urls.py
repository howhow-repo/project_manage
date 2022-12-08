from django.urls import path
from .views import add_project


urlpatterns = [
    path("add/<str:customer_name>", add_project, name='add_project'),
]
