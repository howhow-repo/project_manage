from django import forms

from .models import Bom, BomItem, NonStandardItem


class BomForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].widget.attrs.update({'class': 'form-control'})
        self.fields['discount'].required = False
        self.fields['status'].required = False
        self.fields['tax'].required = False
        self.fields['discount'].required = False
        self.fields['org_cost'].required = False
        self.fields['final_cost'].required = False
        self.fields['note'].required = False
        self.fields['creator'].required = False
        self.fields['note'].widget.attrs.update({'rows': 2})

    class Meta:
        model = Bom
        fields = ('project', 'note', 'discount', 'status', 'org_cost', 'final_cost', 'tax', 'creator')


class BomItemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].widget.attrs.update({'class': 'form-control'})
        self.fields['unit'].required = False
        self.fields['total_price'].required = False

    class Meta:
        model = BomItem
        fields = ('material', 'unit', 'quantity', 'total_price', 'bom')


class BomItemDelForm(forms.Form):
    pass


class NonStandardItemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].widget.attrs.update({'class': 'form-control'})
        self.fields['unit'].required = False
        self.fields['total_price'].required = False

    class Meta:
        model = NonStandardItem
        fields = ('name', 'unit', 'unit_price', 'quantity', 'total_price', 'bom')
