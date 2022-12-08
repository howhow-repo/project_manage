from django import forms
from .models import CustomerType, Customer
# from .models import Project, CaseStatus, Bom, BomItem


class CustomerTypeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].required = False

    class Meta:
        model = CustomerType
        fields = ('name', 'description')


class CustomerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].widget.attrs.update({'class': 'form-control'})
            if f != 'name':
                self.fields[f].required = False

    class Meta:
        model = Customer
        fields = ('name', 'address', 'email', 'tel', 'cel', 'line', 'type', 'note', 'creator', )
