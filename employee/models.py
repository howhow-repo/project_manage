# -*- encoding: utf-8 -*-
import requests
from django.core.validators import MinLengthValidator
from django.db import models
from django.contrib.auth.models import AbstractUser


class Department(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Company(models.Model):
    name = models.CharField(max_length=20)
    tel = models.CharField(max_length=20)
    fax = models.CharField(max_length=20, null=True)
    email = models.EmailField(null=True)
    mail_addr = models.CharField(max_length=50, null=True)
    business_addr = models.CharField(max_length=50)


class User(AbstractUser):
    nickname = models.CharField(max_length=10, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.PROTECT, default=None, null=True)
    phone_number = models.CharField(max_length=20, null=True)
    line_account = models.CharField(max_length=20, null=True)
    notify_token = models.CharField(max_length=43, null=True, validators=[MinLengthValidator(43)])
    is_accept = models.BooleanField(default=True)

    def send_line_notify(self, message):
        if not self.notify_token:
            return None
        headers = {"Authorization": f"Bearer {self.notify_token}"}
        data = {'message': message}
        response = requests.post("https://notify-api.line.me/api/notify",
                                 headers=headers, data=data)
        return response
