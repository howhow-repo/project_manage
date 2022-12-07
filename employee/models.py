# -*- encoding: utf-8 -*-
from django.core.validators import MinLengthValidator
from django.db import models
from django.contrib.auth.models import AbstractUser


class Department(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class User(AbstractUser):
    nickname = models.CharField(max_length=10, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.PROTECT, default=None, null=True)
    phone_number = models.CharField(max_length=20, null=True)
    line_account = models.CharField(max_length=20, null=True)
    notify_token = models.CharField(max_length=43, null=True, validators=[MinLengthValidator(43)])
    is_accept = models.BooleanField(default=True)

