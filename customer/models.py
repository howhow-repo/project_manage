import uuid

from django.db import models

from employee.models import User


class CustomerType(models.Model):
    name = models.CharField(max_length=20, unique=True)
    description = models.TextField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


class CustomerStatus(models.Model):
    name = models.CharField(max_length=20, unique=True)
    description = models.TextField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


class Customer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=20)
    address = models.CharField(max_length=50)
    email = models.EmailField(null=True, blank=True)
    tel = models.CharField(max_length=20)
    cel = models.CharField(max_length=20)
    line = models.CharField(max_length=20, null=True, blank=True)
    type = models.ForeignKey(CustomerType, on_delete=models.PROTECT, null=True, blank=True)
    status = models.ForeignKey(CustomerStatus, on_delete=models.PROTECT, null=True, blank=True)
    note = models.TextField(max_length=1000, default=None, null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, on_delete=models.PROTECT, related_name='customer_creator')
    editor = models.ForeignKey(User, on_delete=models.PROTECT, related_name='customer_editor')

    def __str__(self):
        return self.name


class FavoriteCustomer(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
