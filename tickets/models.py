import os
import uuid
from datetime import timedelta

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from lib import MyManager
from employee.models import User
from tickets.choises import TicketStatusChoices


class Tickets(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer_name = models.CharField(max_length=20, default="", blank=True, )
    customer_cel = models.CharField(max_length=20, default="", blank=True, )
    customer_address = models.CharField(max_length=50, default="", blank=True, )
    page_expired_datetime = models.DateTimeField(default=timezone.now() + timedelta(days=1))
    customer_text = models.TextField(blank=True)
    comment = models.TextField(blank=True)
    linked_user = models.ForeignKey(User, default=None, null=True, on_delete=models.PROTECT, related_name='user')
    create_datetime = models.DateTimeField(auto_now_add=True)
    modify_datetime = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=TicketStatusChoices.choices, default=TicketStatusChoices.NEW)
    create_user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='creator')

    objects = MyManager

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.customer_cel:
            self.customer_cel.replace(" ", "")  # noqa
        super(Tickets, self).save()

    def delete(self, using=None, keep_parents=False):
        try:
            ticket_photos = TicketPhotos.objects.get(ticket=self)
        except models.ObjectDoesNotExist:
            return
        if ticket_photos.photo1 and os.path.isfile(ticket_photos.photo1.name):
            os.remove(ticket_photos.photo1.name)
        if ticket_photos.photo2 and os.path.isfile(ticket_photos.photo2.name):
            os.remove(ticket_photos.photo2.name)
        if ticket_photos.photo3 and os.path.isfile(ticket_photos.photo3.name):
            os.remove(ticket_photos.photo3.name)
        if ticket_photos.photo4 and os.path.isfile(ticket_photos.photo4.name):
            os.remove(ticket_photos.photo4.name)
        ticket_photos.delete()
        super(Tickets, self).delete()


def validate_image(field_file_obj):
    file_size = field_file_obj.file.size
    megabyte_limit = 8.0
    if file_size > megabyte_limit * 1024 * 1024:
        raise ValidationError("Max file size is %sMB" % str(megabyte_limit))


def update_ticket_photo(instance, filename) -> str:
    file_extension = filename.split('.')[-1]
    return settings.DOCS_ROOT + '/Ticket/%s/img.%s' % (instance.ticket.id, file_extension)


class TicketPhotos(models.Model):
    ticket = models.ForeignKey(Tickets, on_delete=models.PROTECT)
    photo1 = models.ImageField(upload_to=update_ticket_photo, validators=[validate_image])
    photo2 = models.ImageField(upload_to=update_ticket_photo, validators=[validate_image])
    photo3 = models.ImageField(upload_to=update_ticket_photo, validators=[validate_image])
    photo4 = models.ImageField(upload_to=update_ticket_photo, validators=[validate_image])
    objects = MyManager()

    @property
    def paths(self):
        l = []
        for k, v in self.__dict__.items():
            if k in ('photo1', 'photo2', 'photo3', 'photo4') and v:
                l.append(v)
        return l

    @property
    def path_count(self):
        return len(self.paths)

    @property
    def path_index(self):
        l = []
        if self.photo1:
            l.append(1)
        if self.photo2:
            l.append(2)
        if self.photo3:
            l.append(3)
        if self.photo4:
            l.append(4)
        return l

    def delete_related_photos(self):
        field_names = ('photo1', 'photo2', 'photo3', 'photo4')
        for name in field_names:
            f = getattr(self, name).name
            if f and os.path.isfile(f):
                os.remove(f)
