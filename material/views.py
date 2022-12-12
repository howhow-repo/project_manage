from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Material


def list_materials(request):
    context = {'material': Material.objects.all()}
    return render(request, 'list_materials.html', context)


@login_required(login_url="/login/")
def add_material(request):
    pass  # TODO


@login_required(login_url="/login/")
def delete_material(request):
    pass  # TODO


@login_required(login_url="/login/")
def material_detail(request):
    pass  # TODO
