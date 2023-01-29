from django.urls import path
from .views import list_bom, add_bom, edit_bom, add_bom_item, del_bom_item, del_bom, freeze_bom, sign_bom
from .views import add_nonstandard_item, del_nonstandard_item, download_xlsx

urlpatterns = [
    path("<str:project_id>/list", list_bom, name='list_bom'),
    path("<str:project_id>/add", add_bom, name='add_bom'),
    path("edit/<str:bom_id>", edit_bom, name='edit_bom'),

    path("edit/<str:bom_id>/add_item", add_bom_item, name='add_bom_item'),
    path("edit/<str:bom_id>/del_item/<str:bom_item_id>", del_bom_item, name='del_bom_item'),

    path("edit/<str:bom_id>/add_nonstandard_item", add_nonstandard_item, name='add_nonstandard_item'),
    path("edit/<str:bom_id>/del_nonstandard_item/<str:bom_item_id>", del_nonstandard_item, name='del_nonstandard_item'),

    path("edit/<str:bom_id>/del_bom", del_bom, name='del_bom'),
    path("edit/<str:bom_id>/freeze_bom", freeze_bom, name='freeze_bom'),
    path("edit/<str:bom_id>/sign_bom", sign_bom, name='sign_bom'),
    path("edit/<str:bom_id>/download_xlsx", download_xlsx, name='download_xlsx'),
]
