# -*- encoding: utf-8 -*-
from django.middleware.csrf import get_token
from django.http import HttpResponseRedirect, JsonResponse, HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet

from permissions import IsManager
from .choises import TicketStatusChoices
from .models import Tickets, TicketPhotos
from .forms import EmployeeEditTicketForm, CustomerEditTicketForm, CustomerEditTicketPhotoForm


class TicketsViewsSet(GenericViewSet):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsManager]
    queryset = Tickets.objects.all()
    photos = TicketPhotos

    segment = {'segment': 'tickets'}

    def list(self, request):
        context = {'tickets': self.queryset.order_by('create_datetime')}
        context.update(self.segment)
        return render(request, 'list_tickets.html', context)

    @action(detail=False, methods=['post'], url_path='new_ticket', url_name='new_ticket')
    def new_ticket(self, request):
        new_ticket = Tickets(create_user=request.user)
        new_ticket.save()
        photo_sheet, _ = self.photos.objects.get_or_create(ticket=new_ticket)
        # return new_ticket.id
        return JsonResponse({'id': new_ticket.id})

    @action(detail=True, methods=['get', 'post'], url_path='employee_update', url_name='employee_update')
    def employee_update(self, request, pk):
        ticket = self.queryset.get(id=pk)
        photos, _ = self.photos.objects.get_or_create(ticket=ticket)
        if request.method == "POST":
            form = EmployeeEditTicketForm(data=request.POST, instance=ticket)
            if form.is_valid():
                form.save()
        else:
            form = EmployeeEditTicketForm(instance=ticket)
        context = {'ticket': ticket, 'photos': photos.path_index, 'form': form}
        context.update(self.segment)
        return render(request, 'ticket_detail.html', context)

    @action(detail=True, methods=['get', 'post'], permission_classes=[], authentication_classes=[],
            url_path='customer_update', url_name='customer_update')
    def customer_update(self, request, pk):
        ticket = self.queryset.get(id=pk)
        if timezone.now() > ticket.page_expired_datetime:
            return render(request, 'edit_expired.html', self.segment)
        photo_sheet, _ = self.photos.objects.get_or_create(ticket=ticket)
        form = CustomerEditTicketForm(instance=ticket)
        Msg = None
        errMsg = None

        if request.method == "POST":
            form = CustomerEditTicketForm(instance=ticket, data=request.POST)
            photo_form = CustomerEditTicketPhotoForm(
                ticket=ticket, instance=photo_sheet,
                data=request.POST, files=request.FILES
            )
            if form.is_valid() and photo_form.is_valid():
                ticket = form.save(commit=False)
                ticket.status = TicketStatusChoices.FILL
                ticket.save()
                photo_sheet = photo_form.save()
                Msg = 'Success Saved'
            else:
                errMsg = f"Error when Saving data."

        context = {
            'ticket': ticket, 'photos': photo_sheet.path_index,
            'form': form, 'photo_form': CustomerEditTicketPhotoForm(ticket=ticket),
            'Msg': Msg, 'errMsg': errMsg
        }

        context.update(self.segment)
        return render(request, 'customer_fill.html', context)

    @action(detail=True, methods=['get'], url_path='confirm_delete', url_name='confirm_delete')
    def confirm_delete(self, request, pk):
        ticket = self.queryset.get(id=pk)
        context = {'ticket': ticket}
        context.update(self.segment)
        return render(request, 'delete_confirm.html', context)

    @method_decorator(csrf_protect)
    @action(detail=True, methods=['post'], url_path='delete', url_name='delete')
    def delete_ticket(self, request, pk):
        ticket = self.queryset.get(id=pk)
        ticket.delete()
        return HttpResponseRedirect(reverse('tickets-list'))
