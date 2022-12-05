from django.db import models

from employee.models import User


class MaterialType(models.Model):
    name = models.CharField(max_length=20, unique=True)
    note = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Material(models.Model):
    name = models.CharField(max_length=20, unique=True)
    type = models.ForeignKey(MaterialType, on_delete=models.PROTECT)
    unit = models.CharField(max_length=10)
    unit_price = models.IntegerField(null=True, blank=True,)
    note = models.CharField(max_length=100, null=True, blank=True,)
    creator = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True,)
    update_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
