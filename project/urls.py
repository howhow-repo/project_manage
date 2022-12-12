from django.urls import path
from .views import list_projects, add_project, project_detail, add_daily_report


urlpatterns = [
    path("", list_projects, name="list_projects"),
    path("<str:customer_name>/addProject", add_project, name='add_project'),
    path("<str:project_id>", project_detail, name='project_detail'),
    path("<str:project_id>/addDailyReport", add_daily_report, name='add_daily_report'),
]
