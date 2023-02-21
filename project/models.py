import uuid
from datetime import datetime, timedelta
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils import timezone

from customer.models import Customer
from employee.models import User


def update_report_photo(instance, filename) -> str:
    file_extension = filename.split('.')[-1]
    return settings.DOCS_ROOT + '/Project/photo/%s.%s' % (instance.report.id, file_extension)


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
    address = models.CharField(max_length=50, default=None, null=True, blank=True)
    status = models.ForeignKey(ProjectStatus, on_delete=models.PROTECT)
    note = models.TextField(max_length=1000, default=None, null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.PROTECT, related_name='project_creator', )
    owner = models.ForeignKey(User, on_delete=models.PROTECT, related_name='project_owner',
                              default=None, null=True, blank=True)
    editor = models.ForeignKey(User, on_delete=models.PROTECT, related_name='project_editor')
    start_date = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField(default=None, null=True, blank=True)
    dispatch_date = models.DateTimeField(default=None, null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_calendar_day_range(self):
        start_date = self.dispatch_date
        if not start_date:
            start_date = self.start_date

        if self.due_date and self.due_date > start_date:
            due_date = self.due_date
        else:
            due_date = start_date + timedelta(hours=1)

        start_date_str = datetime.strftime(start_date, '%Y%m%dT%H%M00')
        due_date_str = datetime.strftime(due_date, '%Y%m%dT%H%M00')

        return start_date_str, due_date_str

    def google_calendar_event(self, request):
        """
        http://www.google.com/calendar/event?
        action=TEMPLATE
        &text=[事件名稱]
        &dates=[開始時間]/[結束時間]                           //時間格式為 YYYYMMDDTHHMMSS
        &details=[詳細的描述]                                //使用 %0A 作為跳行
        &location=[地點]

        :return:
            str: url link
        """
        link = 'http://www.google.com/calendar/event?action=TEMPLATE'
        link += f"&text=[{self.customer.name}]{self.title}-{self.type}"

        start_date_str, due_date_str = self.get_calendar_day_range()
        link += f"&dates={start_date_str}/{due_date_str}"

        add_daily_report_link = self.create_add_report_link(request)
        note_str = f"[{self.customer.name}]\n" \
                   f"  聯絡電話：{self.customer.tel}\n" \
                   f"  手機：{self.customer.cel}\n" \
                   f"  新增紀錄：{add_daily_report_link}\n" \
                   f"----\n\n{self.note}"
        note_str = note_str.replace("\n", r"%0A")
        link += f'&details={note_str}'

        if self.address:
            link += f'&location={self.address}'
        else:
            link += f'&location={self.customer.address}'
        link += '&trp=true'
        return link

    def create_detail_link(self, request):
        return f"http://{request.get_host()}" + reverse('project_detail', kwargs={'project_id': self.id})

    def create_add_report_link(self, request):
        return f"http://{request.get_host()}" + reverse('add_daily_report', kwargs={'project_id': self.id})


class DailyReport(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(Project, on_delete=models.PROTECT)
    note = models.TextField(max_length=1000, null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.PROTECT)
    update_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.project.__str__() + f" report at {self.update_time}"


class DailyReportPhoto(models.Model):
    report = models.ForeignKey(DailyReport, on_delete=models.PROTECT)
    photo1 = models.ImageField(upload_to=update_report_photo, validators=[validate_image])
    photo2 = models.ImageField(upload_to=update_report_photo, validators=[validate_image])
    photo3 = models.ImageField(upload_to=update_report_photo, validators=[validate_image])
    photo4 = models.ImageField(upload_to=update_report_photo, validators=[validate_image])
    photo5 = models.ImageField(upload_to=update_report_photo, validators=[validate_image])
    photo6 = models.ImageField(upload_to=update_report_photo, validators=[validate_image])


class DailyReportComment(models.Model):
    daily_report = models.ForeignKey(DailyReport, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    comment = models.CharField(max_length=50)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.daily_report.__str__() + f" comment"


class FavoriteProject(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    project = models.ForeignKey(Project, on_delete=models.PROTECT)
