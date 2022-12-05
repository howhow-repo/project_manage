from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from employee.models import User
from materials.models import Material


def update_case_img(instance, filename) -> str:
    filename_ = instance.name
    file_extension = filename.split('.')[-1]
    return settings.DOCS_ROOT + '/Case/img/%s.%s' % (filename_, file_extension)


def validate_image(field_file_obj):
    file_size = field_file_obj.file.size
    megabyte_limit = 5.0
    if file_size > megabyte_limit * 1024 * 1024:
        raise ValidationError("Max file size is %sMB" % str(megabyte_limit))


class CustomerType(models.Model):
    name = models.CharField(max_length=20, unique=True)
    description = models.TextField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


class CaseStatus(models.Model):
    name = models.CharField(max_length=20, unique=True)
    description = models.TextField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


class Customer(models.Model):
    name = models.CharField(max_length=20)
    address = models.CharField(max_length=50)
    email = models.EmailField()
    tel = models.CharField(max_length=20)
    cel = models.CharField(max_length=20)
    line = models.CharField(max_length=20)
    type = models.ForeignKey(CustomerType, on_delete=models.PROTECT)
    note = models.TextField(max_length=500)
    update_time = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class Case(models.Model):
    title = models.CharField(max_length=20)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    status = models.ForeignKey(CaseStatus, on_delete=models.PROTECT)
    note = models.TextField(max_length=500)
    creator = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.title


class DailyReport(models.Model):
    title = models.CharField(max_length=20)
    case = models.ForeignKey(Case, on_delete=models.PROTECT)
    note = models.TextField(max_length=500)
    update_time = models.DateTimeField(auto_now_add=True)
    update_person = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.case.__str__() + f"at {self.update_time}"


class Bom(models.Model):
    case = models.ForeignKey(Case, on_delete=models.PROTECT)
    note = models.TextField(max_length=500)
    discount = models.FloatField()
    org_cost = models.FloatField()
    final_cost = models.IntegerField()
    creator = models.ForeignKey(User, on_delete=models.PROTECT)
    update_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.case.__str__()


class BomItem(models.Model):
    material = models.ForeignKey(Material, on_delete=models.PROTECT)
    unit = models.CharField(max_length=10)
    quantity = models.FloatField(max_length=99999)
    price = models.FloatField(1_0000_0000)

    def __str__(self):
        return self.material.__str__()


class DailyReportImages(models.Model):
    case = models.ForeignKey(Case, on_delete=models.PROTECT)
    image1 = models.ImageField(upload_to=update_case_img, validators=[validate_image])
    image2 = models.ImageField(upload_to=update_case_img, validators=[validate_image])
    image3 = models.ImageField(upload_to=update_case_img, validators=[validate_image])
    image4 = models.ImageField(upload_to=update_case_img, validators=[validate_image])
    image5 = models.ImageField(upload_to=update_case_img, validators=[validate_image])
