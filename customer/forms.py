from django import forms
from .models import CustomerType, Customer, FavoriteCustomer
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
        fields = ('name', 'address', 'email', 'tel', 'cel', 'line', 'type', 'status', 'note', 'creator', )


class FavoriteCustomerForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.Meta.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        self.fields['user'].required = False
        self.fields['customer'].required = False

    class Meta:
        model = FavoriteCustomer
        fields = ['user', 'customer']

    def set_initial(self, user, customer_id):
        self.fields['user'].initial = user
        self.fields['customer'].initial = customer_id
