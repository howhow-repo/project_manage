from django import forms
from .models import DailyReport, DailyReportImages, ProjectStatus, Project


class ProjectStatusForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].required = False

    class Meta:
        model = ProjectStatus
        fields = ('name', 'description')


class ProjectForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].widget.attrs.update({'class': 'form-control'})
        self.fields['note'].required = False
        self.fields['owner'].required = False
        self.fields['creator'].required = False
        self.fields['customer'].required = False

    class Meta:
        model = Project
        fields = ('title', 'customer', 'status', 'note', 'owner', 'creator', 'due_date', 'start_date')


class DailyReportForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].widget.attrs.update({'class': 'form-control'})
            if f != 'project':
                self.fields[f].required = False

    class Meta:
        model = DailyReport
        fields = ('title', 'project', 'note', 'update_person')


class DailyReportImagesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].widget.attrs.update({'class': 'form-control'})
            if f != 'project':
                self.fields[f].required = False

    class Meta:
        model = DailyReportImages
        fields = ('project', 'image1', 'image2', 'image3', 'image4', 'image5')
