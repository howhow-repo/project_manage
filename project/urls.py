from django.urls import path
from .views import add_project, project_detail


urlpatterns = [
    path("<str:customer_name>/add", add_project, name='add_project'),
    path("<str:project_id>", project_detail, name='project_detail'),
]
