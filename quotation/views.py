# -*- encoding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound, HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse

from project.models import Project
from .models import Bom, BomItem, NonStandardItem
from .form import BomForm, BomItemForm, BomItemDelForm, NonStandardItemForm
from lib import get_model_or_none


@login_required(login_url="/login/")
def save_new_bom_or_none(request, project):
    form = BomForm(data=request.POST)
    if form.is_valid():
        new_bom = form.save(commit=False)
        new_bom.project, new_bom.creator, new_bom.editor = project, request.user, request.user
        new_bom.create_sn()
        new_bom.save()
        return new_bom
    else:
        print(form.errors.as_data())
    return None


@login_required(login_url="/login/")
def list_bom(request, project_id):
    project = get_model_or_none(Project, {'id': project_id})
    if not project:
        return HttpResponseNotFound()

    context = {'segment': 'project', 'project': project}
    bom_list = Bom.objects.filter(project=project)
    if not bom_list:
        context['empty'] = True
    context['bom_list'] = bom_list
    return render(request, 'list_bom.html', context)


@login_required(login_url="/login/")
def add_bom(request, project_id):
    project = get_model_or_none(Project, {'id': project_id})
    if not project:
        return HttpResponseNotFound()

    context = {'segment': 'project'}
    # Do POST
    if request.method == "POST":
        bom_form = BomForm(data=request.POST)
        new_bom = save_new_bom_or_none(request, project)
        if new_bom:
            context['Msg'] = 'Success'
            return HttpResponseRedirect(reverse('edit_bom', kwargs={'bom_id': new_bom.id}))
        else:
            context['errMsg'] = 'Form is not valid'

    # Do GET
    else:
        bom_form = BomForm()
    bom_form.fields['project'].initial = project
    context.update({
        'bom_form': bom_form,
        'project': project,
    })
    return render(request, 'add_bom.html', context)


@login_required(login_url="/login/")
def edit_bom(request, bom_id):
    bom = get_model_or_none(Bom, {'id': bom_id})
    if not bom:
        return HttpResponseNotFound()
    context = {'segment': 'project'}

    # Do POST
    if request.method == "POST":
        bom_form = BomForm(data=request.POST, instance=bom)
        if bom_form.is_valid():
            new_bom = bom_form.save(commit=False)
            new_bom.editor = request.user
            new_bom.calculate_bom()
            new_bom.save()
            context['Msg'] = 'Success'

        else:
            context['errMsg'] = 'Form is not valid'
    else:
        bom_form = BomForm(instance=bom)

    # Do GET
    bom_item_form, nonstandard_item_form = BomItemForm(), NonStandardItemForm()
    bom_item_form.fields['bom'].initial, nonstandard_item_form.fields['bom'].initial = bom, bom
    bom_item_form.fields['quantity'].initial = 1
    context.update({
        'form': bom_form,
        'item_form': bom_item_form,
        'nonstandard_item_form': nonstandard_item_form,
        'bom': bom,
        'bom_items': BomItem.objects.filter(bom=bom),
        'nonstandard_item': NonStandardItem.objects.filter(bom=bom),
    })
    return render(request, 'edit_bom.html', context)


@login_required(login_url="/login/")
def add_bom_item(request, bom_id):
    bom = get_model_or_none(Bom, {'id': bom_id})
    if not bom:
        return HttpResponseNotFound()

    if request.method == "POST":
        form = BomItemForm(data=request.POST)
        if form.is_valid():
            new_item = form.save(commit=False)
            new_item.freeze_material_info()
            new_item.calculate_price()
            new_item.save()
            bom.calculate_bom()
            bom.set_editor(request)
            bom.save()

    return HttpResponseRedirect(reverse('edit_bom', kwargs={'bom_id': bom.id}))


@login_required(login_url="/login/")
def del_bom_item(request, bom_id, bom_item_id):
    bom = get_model_or_none(Bom, {'id': bom_id})
    if not bom:
        return HttpResponseNotFound()
    if request.method == "POST":
        form = BomItemDelForm(data=request.POST)
        if form.is_valid():
            item = BomItem.objects.get(id=bom_item_id)
            item.delete()
            bom.calculate_bom()
            bom.set_editor(request)
            bom.save()
    return HttpResponseRedirect(reverse('edit_bom', kwargs={'bom_id': bom.id}))


@login_required(login_url="/login/")
def add_nonstandard_item(request, bom_id):
    bom = get_model_or_none(Bom, {'id': bom_id})
    if not bom:
        return HttpResponseNotFound()
    if request.method == "POST":
        form = NonStandardItemForm(data=request.POST)
        if form.is_valid():
            new_item = form.save(commit=False)
            new_item.calculate_price()
            new_item.save()
            bom.calculate_bom()
            bom.set_editor(request)
            bom.save()
    return HttpResponseRedirect(reverse('edit_bom', kwargs={'bom_id': bom.id}))


@login_required(login_url="/login/")
def del_nonstandard_item(request, bom_id, bom_item_id):
    bom = get_model_or_none(Bom, {'id': bom_id})
    if not bom:
        return HttpResponseNotFound()
    if request.method == "POST":
        form = BomItemDelForm(data=request.POST)
        if form.is_valid():
            item = NonStandardItem.objects.get(id=bom_item_id)
            item.delete()
            bom.calculate_bom()
            bom.set_editor(request)
            bom.save()
    return HttpResponseRedirect(reverse('edit_bom', kwargs={'bom_id': bom.id}))


def del_bom(request, bom_id):
    pass


@login_required(login_url="/login/")
def download_xlsx(request, bom_id):
    bom = get_model_or_none(Bom, {'id': bom_id})
    if not bom:
        return HttpResponseNotFound()

    response = HttpResponse(content=bom.create_xlsx(request),
                            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=quotation_{bom.sn}.xlsx'
    return response
