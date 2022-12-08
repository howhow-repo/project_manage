from django.urls import path
from .views import list_customers, customer_detail, add_customer


urlpatterns = [
    path("", list_customers, name='list_customers'),
    path("add", add_customer, name='add_customer'),
    path("<str:cust_name>", customer_detail, name="customer_detail")
]
