from django import forms
from .models import Material, MaterialType


class MaterialTypeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].widget.attrs.update({'class': 'form-control'})
        self.fields['note'].required = False

    class Meta:
        model = MaterialType
        fields = ('name', 'note')


class MaterialForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].widget.attrs.update({'class': 'form-control'})
        self.fields['note'].required = False
        self.fields['creator'].required = False
        self.fields['note'].required = False

    class Meta:
        model = Material
        fields = ('name', 'part_number', 'cover', 'type', 'unit', 'unit_price', 'note', 'creator')


class MaterialTypeDelForm(forms.Form):
    pass


class MaterialDelForm(forms.Form):
    pass
