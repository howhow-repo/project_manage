from django.urls import path
from .views import list_customers, customer_detail, add_customer, pre_add_customer, search_customers

urlpatterns = [
    path("", list_customers, name='list_customers'),
    path("search", search_customers, name='search_customers'),
    path("pre_add", pre_add_customer, name='pre_add_customer'),
    path("add", add_customer, name='add_customer'),
    path("<str:cust_id>", customer_detail, name="customer_detail")
]
