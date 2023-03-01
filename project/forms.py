from django import forms
from .models import DailyReport, DailyReportPhoto, ProjectStatus, Project, FavoriteProject


class DateInput(forms.DateInput):
    input_type = 'date'


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
            if f != 'title' and f != 'status':
                self.fields[f].required = False

    class Meta:
        model = Project
        fields = (
            'title', 'type', 'customer', 'address', 'status', 'note', 'owner', 'creator', 'due_date', 'start_date', 'dispatch_date')
        widgets = {
            'dispatch_date': DateInput(),
            'start_date': DateInput(),
            'due_date': DateInput(),
        }


class DailyReportForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].widget.attrs.update({'class': 'form-control'})
            if f != 'project':
                self.fields[f].required = False

    class Meta:
        model = DailyReport
        fields = ('project', 'note', 'creator')


class DailyReportPhotoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].widget.attrs.update({'class': 'form-control'})
            if f != 'project':
                self.fields[f].required = False

    class Meta:
        model = DailyReportPhoto
        fields = ('report', 'photo1', 'photo2', 'photo3', 'photo4', 'photo5', 'photo6')


class FavoriteProjectForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.Meta.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        self.fields['user'].required = False
        self.fields['project'].required = False

    class Meta:
        model = FavoriteProject
        fields = ['user', 'project']

    def set_initial(self, user, project_id):
        self.fields['user'].initial = user
        self.fields['project'].initial = project_id
