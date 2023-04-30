import os

from django import forms
from .models import Tickets, TicketPhotos


class CustomerEditTicketForm(forms.ModelForm):
    required_fields = ['customer_name', 'customer_cel', 'customer_address', 'customer_text']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.Meta.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
            if field not in self.required_fields:
                self.fields[field].required = False

    class Meta:
        model = Tickets
        fields = ['customer_name', 'customer_cel', 'customer_address', 'customer_text']


class EmployeeEditTicketForm(forms.ModelForm):
    required_fields = ['comment', 'status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.Meta.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
            if field not in self.required_fields:
                self.fields[field].required = False

    class Meta:
        model = Tickets
        fields = ['comment', 'status']


class CustomerEditTicketPhotoForm(forms.ModelForm):
    required_fields = ['tickets']

    def __init__(self, ticket: Tickets, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ticket'].initial = ticket
        for field in self.Meta.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
            if field not in self.required_fields:
                self.fields[field].required = False

    class Meta:
        model = TicketPhotos
        fields = ['ticket', 'photo1', 'photo2', 'photo3', 'photo4']

    # def remove_sensitive_information(self):
    #     form_name = ['photo1', 'photo2', 'photo3', 'photo4']
    #     for name in form_name:
    #         self.initial[name].initial = None
    #     return self

    def save(self, commit=True):
        photo_field_names = ['photo1', 'photo2', 'photo3', 'photo4']
        old_instance = TicketPhotos.objects.get(id=self.instance.id)
        old_file_paths = []
        for field in self.changed_data:
            if field in photo_field_names:
                old_file_paths.append(getattr(old_instance, field).name)

        instance = super().save(commit=commit)
        for path in old_file_paths:
            if path and os.path.isfile(path):
                os.remove(path)

        return instance
