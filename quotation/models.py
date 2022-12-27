import math
import uuid
from datetime import timedelta

import openpyxl
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Sum
from django.utils import dateformat, timezone
from django.conf import settings

from employee.models import User
from material.models import Material
from project.models import Project


class BomStatus(models.Model):
    name = models.CharField(max_length=12, unique=True)
    note = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.name


class Bom(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(Project, on_delete=models.PROTECT)
    sn = models.CharField(max_length=12, null=True, unique=True)
    status = models.ForeignKey(BomStatus, on_delete=models.PROTECT, default=1)
    note = models.TextField(max_length=500)
    discount = models.FloatField(default=1.0, validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    org_cost = models.FloatField(default=0, validators=[MinValueValidator(0), ])
    tax = models.FloatField(default=0, validators=[MinValueValidator(0), ])
    final_cost = models.IntegerField(default=0, validators=[MinValueValidator(0), ])
    editor = models.ForeignKey(User, on_delete=models.PROTECT, related_name='bom_editor')
    creator = models.ForeignKey(User, on_delete=models.PROTECT, related_name='bom_creator')
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'bom' + self.project.__str__()

    def create_sn(self):
        utc_now = timezone.now()
        local_now = utc_now.today()
        today_begin = utc_now - timedelta(
            hours=local_now.hour,
            minutes=local_now.minute,
            seconds=local_now.second,
            microseconds=local_now.microsecond
        )
        data_count = Bom.objects.filter(create_time__range=[today_begin, utc_now]).count()
        self.sn = f"{dateformat.format(timezone.now(), 'Ymd')}{str(data_count + 1).zfill(2)}"

    def calculate_bom(self):
        standard_cost = (BomItem.objects.filter(bom=self).aggregate(Sum('total_price')))['total_price__sum'] or 0
        nonstandard_cost = (NonStandardItem.objects.filter(bom=self).aggregate(Sum('total_price')))[
                               'total_price__sum'] or 0
        self.org_cost = standard_cost + nonstandard_cost
        self.tax = self.org_cost * 5 / 100 * self.discount
        self.final_cost = math.ceil((self.org_cost * self.discount) + self.tax)

    def set_editor(self, request):
        self.editor = request.user

    def create_xlsx(self, request):
        q_template = openpyxl.load_workbook(f'{settings.BASEDIR}/quotation/quotation_template.xlsx')
        q_template.worksheets[0]['B4'] = f'NO.{self.sn}'
        q_template.worksheets[0]['E4'] = f'NO.{request.user.nickname}'
        q_template.worksheets[0]['B8'] = self.project.customer.name
        q_template.worksheets[0]['B9'] = self.project.customer.name
        q_template.worksheets[0]['B10'] = self.project.address
        q_template.worksheets[0]['F7'] = timezone.now().today().date()
        return q_template


class BomItem(models.Model):
    bom = models.ForeignKey(Bom, on_delete=models.PROTECT)
    material = models.ForeignKey(Material, on_delete=models.PROTECT)
    freeze_material_name = models.CharField(max_length=20, null=True, blank=True)
    unit = models.CharField(max_length=10)
    quantity = models.FloatField(max_length=99999, validators=[MinValueValidator(0), ])
    freeze_material_price = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0), ])
    total_price = models.FloatField(validators=[MinValueValidator(0), ])

    def __str__(self):
        return self.material.__str__()

    def freeze_material_info(self):
        self.freeze_material_name = self.material.name
        self.freeze_material_price = self.material.unit_price

    def calculate_price(self):
        self.total_price = self.quantity * self.freeze_material_price


class NonStandardItem(models.Model):
    bom = models.ForeignKey(Bom, on_delete=models.PROTECT)
    name = models.CharField(max_length=20, null=True, blank=True)
    unit = models.CharField(max_length=10)
    unit_price = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0), ])
    quantity = models.FloatField(max_length=99999, validators=[MinValueValidator(0), ])
    total_price = models.FloatField(validators=[MinValueValidator(0), ])

    def calculate_price(self):
        self.total_price = self.quantity * self.unit_price
