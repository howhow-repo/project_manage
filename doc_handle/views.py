# -*- encoding: utf-8 -*-
import os

from django.db import models
from django.http import HttpResponse, HttpResponseNotFound
from django.utils import timezone

from material.models import Material
from django.contrib.auth.decorators import login_required
from django.conf import settings

from project.models import DailyReportPhoto
from tickets.models import TicketPhotos, Tickets

video_extension = ['mp4', 'mov']
doc_extension = ['pdf']


def find_path_by_order(photo_sets, photo_num):
    stack = []
    for photo_set in photo_sets:
        for k, v in photo_set.__dict__.items():
            if 'photo' in k and v:
                stack.append(v)
    try:
        return stack[photo_num]
    except IndexError:
        return None


@login_required(login_url="/login/")
def get_daily_report_photo(request, report_id, photo_num):
    try:
        photo_sets = DailyReportPhoto.objects.filter(report=report_id).order_by('id')
    except models.ObjectDoesNotExist:
        return HttpResponseNotFound()

    path = find_path_by_order(photo_sets, photo_num)

    if path and os.path.isfile(path):
        with open(path, "rb") as file:
            return HttpResponse(file.read(), content_type="image/jpeg")

    return HttpResponseNotFound()


@login_required(login_url="/login/")
def get_material_cover(request, material_id):
    try:
        material = Material.objects.get(id=material_id)
    except models.ObjectDoesNotExist:
        return HttpResponseNotFound()

    path = material.cover.name

    if path and os.path.isfile(path):
        with open(path, "rb") as file:
            return HttpResponse(file.read(), content_type="image/jpeg")

    with open(settings.STATICFILES_DIRS[0] + '/assets/images/default_material_cover.png', "rb") as file:
        return HttpResponse(file.read(), content_type="image/jpeg")


def get_ticket_photo(request, ticket_id, photo_num):
    try:
        ticket = Tickets.objects.get(id=ticket_id)
        ticket_photos = TicketPhotos.objects.get(ticket=ticket_id)
    except models.ObjectDoesNotExist:
        return HttpResponseNotFound()
    if timezone.now() > ticket.page_expired_datetime:
        return HttpResponseNotFound()

    path = getattr(ticket_photos, f"photo{photo_num}")

    if path and os.path.isfile(path.name):
        with open(path.name, "rb") as file:
            return HttpResponse(file.read(), content_type="image/jpeg")

    return HttpResponseNotFound()
