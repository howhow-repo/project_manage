from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import dateformat, timezone

from employee.models import User
from material.models import Material
from project.models import Project


class Bom(models.Model):
    case = models.ForeignKey(Project, on_delete=models.PROTECT)
    sn = models.CharField(max_length=12, null=True, unique=True)
    note = models.TextField(max_length=500)
    discount = models.FloatField(default=1.0, validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],)
    org_cost = models.FloatField()
    tax = models.FloatField()
    final_cost = models.IntegerField()
    creator = models.ForeignKey(User, on_delete=models.PROTECT)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'bom' + self.case.__str__()

    def __int__(self):
        if not self.sn:
            data_count = self.objects.filter(update_time=timezone.now().today()).count()
            self.sn = f"{dateformat.format(timezone.now(), 'Ymd')}{str(data_count+1).zfill(3)}"


class BomItem(models.Model):
    material = models.ForeignKey(Material, on_delete=models.PROTECT)
    unit = models.CharField(max_length=10)
    quantity = models.FloatField(max_length=99999)
    price = models.FloatField()

    def __str__(self):
        return self.material.__str__()
