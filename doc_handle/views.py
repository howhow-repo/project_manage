# -*- encoding: utf-8 -*-
import os
from django.http import HttpResponse, HttpResponseNotFound

from material.models import Material
from django.contrib.auth.decorators import login_required
from django.conf import settings

from project.models import DailyReportPhoto

video_extension = ['mp4', 'mov']
doc_extension = ['pdf']


def find_path_by_order(photo_sets, photo_num):
    counter = 0
    for photo_set in photo_sets:
        for k in photo_set.__dict__.keys():
            if 'photo' in k and getattr(photo_set, k):
                if counter == photo_num:
                    return getattr(photo_set, k)
                counter += 1

                if counter > photo_num:
                    return None
    return None


@login_required(login_url="/login/")
def get_daily_report_photo(request, report_id, photo_num):
    try:
        photo_sets = DailyReportPhoto.objects.filter(report=report_id).order_by('id')

    except Exception:
        return HttpResponseNotFound()

    path = find_path_by_order(photo_sets, photo_num)

    if path and os.path.isfile(path.name):
        with open(path.name, "rb") as file:
            return HttpResponse(file.read(), content_type="image/jpeg")

    return HttpResponseNotFound()


@login_required(login_url="/login/")
def get_material_cover(request, material_id):
    try:
        material = Material.objects.get(id=material_id)
    except Exception:
        return HttpResponseNotFound()

    path = material.cover

    if path and os.path.isfile(path.name):
        with open(path.name, "rb") as file:
            return HttpResponse(file.read(), content_type="image/jpeg")

    with open(settings.STATICFILES_DIRS[0] + '/assets/images/default_material_cover.png', "rb") as file:
        return HttpResponse(file.read(), content_type="image/jpeg")
