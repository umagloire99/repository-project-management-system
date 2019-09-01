from bootstrap_datepicker_plus import DatePickerInput
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from ckeditor.widgets import CKEditorWidget
from django import forms
from .models import *
from django.contrib.admin.widgets import *


class DateInput(forms.DateInput):
    input_type = 'date'


class ProjectForm(forms.ModelForm):
    types = [('In Progress', 'In Progress'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')]
    name = forms.CharField(label='Project Name:')
    description = forms.CharField(label='Description: ', widget=CKEditorUploadingWidget())
    progressbar = forms.IntegerField(label='Progress:')
    category = forms.ChoiceField(choices=types, label='Category: ', widget=forms.Select)

    class Meta:
        model = Project
        fields = ['name', 'icon', 'description', 'progressbar', 'category', 'budget', 'startDate', 'endDate']
        widgets = {
            'startDate': DateInput(),  # default date-format %m/%d/%Y will be used
            'endDate': DateInput(),  # specify date-frmat
        }


class TeamForm(forms.ModelForm):
    role = forms.ModelMultipleChoiceField(
        queryset=Role.objects.all(),
        required=True,
        widget=forms.CheckboxSelectMultiple()
    )

    class Meta:
        model = Team
        fields = ['member', 'role', 'project']


class TaskForm(forms.ModelForm):
    types = [('New', 'New'), ('On Hold', 'On Hold'), ('In Progress', 'In Progress'), ('Completed', 'Completed'),
             ('Cancelled', 'Cancelled')]
    name = forms.CharField(label='Title: ', widget=forms.TextInput(
        attrs={
            'class': 'form-control'
        }
    ))
    description = forms.CharField(label='Description: ', widget=CKEditorWidget(config_name='other'))
    status = forms.ChoiceField(choices=types, label='status', widget=forms.Select(
        attrs={
            'class': 'form-control'
        }
    ))
    member = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=True,
        widget=forms.CheckboxSelectMultiple()
    )

    class Meta:
        model = Task
        fields = ['name', 'description', 'project', 'status', 'member', 'start_date', 'due_date']
        widgets = {
            'start_date': DateInput(attrs={'class': 'form-control'}),  # default date-format %m/%d/%Y will be used
            'due_date': DateInput(attrs={'class': 'form-control'}),  # specify date-frmat
        }


class FileForm(forms.ModelForm):
    note = forms.CharField(label='note',widget=CKEditorWidget(config_name='short'))
    file_name = forms.CharField(label='', widget=forms.TextInput(
        attrs={
            'class': 'form-control'
        }
    ))

    class Meta:
        model = FileManager
        fields = ['file_name', 'upload_file', 'note', 'project']


class InventoryForm(forms.ModelForm):
    note = forms.CharField(label='note', required=True, widget=CKEditorWidget(config_name='short'))
    item = forms.CharField(label='Title: ', widget=forms.TextInput(
        attrs={
            'class': 'form-control'
        }
    ))
    cost = forms.IntegerField(label='Title: ', widget=forms.NumberInput(
        attrs={
            'class': 'form-control'
        }
    ))
    quantity = forms.IntegerField(label='Title: ', widget=forms.NumberInput(
        attrs={
            'class': 'form-control'
        }
    ))

    class Meta:
        model = Inventory
        fields = ['project', 'item', 'cost', 'quantity', 'note']
