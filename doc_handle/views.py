# -*- encoding: utf-8 -*-
import os
from django.http import HttpResponse, HttpResponseNotFound
from .lib import stream_video
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.conf import settings


video_extension = ['mp4', 'mov']
doc_extension = ['pdf']
