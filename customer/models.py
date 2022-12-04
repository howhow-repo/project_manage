from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


def update_case_img(instance, filename) -> str:
    filename_ = instance.name
    file_extension = filename.split('.')[-1]
    return settings.DOCS_ROOT + '/Case/img/%s.%s' % (filename_, file_extension)


def validate_image(fieldfile_obj):
    filesize = fieldfile_obj.file.size
    megabyte_limit = 5.0
    if filesize > megabyte_limit * 1024 * 1024:
        raise ValidationError("Max file size is %sMB" % str(megabyte_limit))


class CustomerType(models.Model):
    name = models.CharField(max_length=20, unique=True)
    description = models.TextField(max_length=100, null=True, blank=True)


class Customer(models.Model):
    name = models.CharField(max_length=20)
    address = models.CharField(max_length=50)
    tel = models.CharField(max_length=20)
    line = models.CharField(max_length=20)
    type = models.ForeignKey(CustomerType, on_delete=models.PROTECT)


class Case(models.Model):
    name = models.CharField(max_length=20)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    note = models.TextField(max_length=500)


class DailyReport(models.Model):
    note = models.TextField(max_length=500)


class BonList(models.Model):
    Case = models.ForeignKey(Case, on_delete=models)


class CaseImage(models.Model):
    case = models.ForeignKey(Case, on_delete=models)
    image1 = models.ImageField(upload_to=update_case_img, validators=[validate_image])
    image2 = models.ImageField(upload_to=update_case_img, validators=[validate_image])
    image3 = models.ImageField(upload_to=update_case_img, validators=[validate_image])
    image4 = models.ImageField(upload_to=update_case_img, validators=[validate_image])
    image5 = models.ImageField(upload_to=update_case_img, validators=[validate_image])
