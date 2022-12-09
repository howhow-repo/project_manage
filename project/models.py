import uuid
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from customer.models import Customer
from employee.models import User


def update_case_img(instance, filename) -> str:
    filename_ = instance.report.id
    file_extension = filename.split('.')[-1]
    return settings.DOCS_ROOT + '/Project/photo/%s.%s' % (filename_, file_extension)


def validate_image(field_file_obj):
    file_size = field_file_obj.file.size
    megabyte_limit = 5.0
    if file_size > megabyte_limit * 1024 * 1024:
        raise ValidationError("Max file size is %sMB" % str(megabyte_limit))


class ProjectStatus(models.Model):
    name = models.CharField(max_length=20, unique=True)
    description = models.TextField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


class ProjectType(models.Model):
    name = models.CharField(max_length=20, unique=True)
    description = models.TextField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=20, default='no title')
    type = models.ForeignKey(ProjectType, on_delete=models.PROTECT, default=None, null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    status = models.ForeignKey(ProjectStatus, on_delete=models.PROTECT)
    note = models.TextField(max_length=1000, default=None, null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.PROTECT, related_name='project_creator', )
    owner = models.ForeignKey(User, on_delete=models.PROTECT, related_name='project_owner',
                              default=None, null=True, blank=True)
    editor = models.ForeignKey(User, on_delete=models.PROTECT, related_name='project_editor')
    start_date = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField(default=None, null=True, blank=True)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class DailyReport(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(Project, on_delete=models.PROTECT)
    note = models.TextField(max_length=500)
    creator = models.ForeignKey(User, on_delete=models.PROTECT)
    update_time = models.DateTimeField(auto_now_add=True)
    image1 = models.ImageField(upload_to=update_case_img, validators=[validate_image], default=None, null=True, blank=True)
    image2 = models.ImageField(upload_to=update_case_img, validators=[validate_image], default=None, null=True, blank=True)
    image3 = models.ImageField(upload_to=update_case_img, validators=[validate_image], default=None, null=True, blank=True)
    image4 = models.ImageField(upload_to=update_case_img, validators=[validate_image], default=None, null=True, blank=True)
    image5 = models.ImageField(upload_to=update_case_img, validators=[validate_image], default=None, null=True, blank=True)

    def __str__(self):
        return self.project.__str__() + f"at {self.update_time}"


class DailyReportImages(models.Model):
    report = models.ForeignKey(DailyReport, on_delete=models.PROTECT)
    image1 = models.ImageField(upload_to=update_case_img, validators=[validate_image])
    image2 = models.ImageField(upload_to=update_case_img, validators=[validate_image])
    image3 = models.ImageField(upload_to=update_case_img, validators=[validate_image])
    image4 = models.ImageField(upload_to=update_case_img, validators=[validate_image])
    image5 = models.ImageField(upload_to=update_case_img, validators=[validate_image])


class DailyReportComment(models.Model):
    daily_report = models.ForeignKey(DailyReport, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    comment = models.CharField(max_length=50)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.daily_report.__str__() + f" comment"
