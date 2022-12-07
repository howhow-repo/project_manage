from django import forms
from .models import CustomerType, Customer
from .models import Case, CaseStatus, Bom, BomItem
from .models import DailyReport, DailyReportImages


class CustomerTypeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].required = False

    class Meta:
        model = CustomerType
        fields = ('name', 'description')


class CaseStatusForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].required = False

    class Meta:
        model = CaseStatus
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
        fields = ('name', 'address', 'email', 'tel', 'cel', 'line', 'type', 'note', 'creator')


class CaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].widget.attrs.update({'class': 'form-control'})
        self.fields['note'].required = False
        self.fields['owner'].required = False

    class Meta:
        model = Case
        fields = ('title', 'customer', 'status', 'note', 'creator')


class DailyReportForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].widget.attrs.update({'class': 'form-control'})
            if f != 'case':
                self.fields[f].required = False

    class Meta:
        model = DailyReport
        fields = ('title', 'case', 'note', 'update_person')


class DailyReportImagesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].widget.attrs.update({'class': 'form-control'})
            if f != 'case':
                self.fields[f].required = False

    class Meta:
        model = DailyReportImages
        fields = ('case', 'image1', 'image2', 'image3', 'image4', 'image5')


class BomForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].widget.attrs.update({'class': 'form-control'})
        self.fields['discount'].required = False

    class Meta:
        model = Bom
        fields = ('case', 'note', 'discount', 'org_cost', 'final_cost', 'creator')


class BomItemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].widget.attrs.update({'class': 'form-control'})
        self.fields['unit'].required = False

    class Meta:
        model = BomItem
        fields = ('material', 'unit', 'quantity', 'price')
