from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from employee.models import User


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
