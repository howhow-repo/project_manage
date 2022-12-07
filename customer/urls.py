from django.urls import path
from .views import list_customers, customer_detail


urlpatterns = [
    path("", list_customers, name='list_customers'),
    path("<str:cust_name>", customer_detail, name="customer_detail")
]
