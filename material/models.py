from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from employee.models import User
from project.models import Project


def update_img(instance, filename) -> str:
    filename_ = instance.name
    file_extension = filename.split('.')[-1]
    return settings.DOCS_ROOT + '/Materials/img/%s.%s' % (filename_, file_extension)


def validate_image(field_file_obj):
    file_size = field_file_obj.file.size
    megabyte_limit = 1.0
    if file_size > megabyte_limit * 1024 * 1024:
        raise ValidationError("Max file size is %sMB" % str(megabyte_limit))


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
    cover = models.ImageField(upload_to=update_img, null=True, blank=True, default=None, validators=[validate_image])
    note = models.CharField(max_length=100, null=True, blank=True,)
    creator = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True,)
    update_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Bom(models.Model):
    case = models.ForeignKey(Project, on_delete=models.PROTECT)
    note = models.TextField(max_length=500)
    discount = models.FloatField(default=1.0, validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],)
    org_cost = models.FloatField()
    final_cost = models.IntegerField()
    creator = models.ForeignKey(User, on_delete=models.PROTECT)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.case.__str__()


class BomItem(models.Model):
    material = models.ForeignKey(Material, on_delete=models.PROTECT)
    unit = models.CharField(max_length=10)
    quantity = models.FloatField(max_length=99999)
    price = models.FloatField()

    def __str__(self):
        return self.material.__str__()
