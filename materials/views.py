from django.shortcuts import render
from .models import Material


def list_materials(request):
    context = {'materials': Material.objects.all()}
    return render(request, 'list_materials.html', context)
