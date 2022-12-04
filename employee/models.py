# -*- encoding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import AbstractUser


class BranchLocation(models.Model):
    name = models.CharField(max_length=20)
    location = models.CharField(max_length=100,  null=True, blank=True)
    tel = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class User(AbstractUser):
    nickname = models.CharField(max_length=10, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.PROTECT, default=None, null=True)
    location = models.ForeignKey(BranchLocation, on_delete=models.PROTECT, default=None, blank=True, null=True)
    phone_number = models.CharField(max_length=20, null=True)
    is_accept = models.BooleanField(default=True)
