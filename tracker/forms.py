import datetime

from django import forms
from django.forms import ModelForm
from django.forms.models import inlineformset_factory

from tracker.models import *


class TimesheetTaskForm(ModelForm):
    duration = forms.DurationField(required=False, widget = forms.TextInput(attrs={'size': 5, 'class': 'clock'}))
    class Meta:
        model = TimesheetTask
        exclude = ('created_at',)
        widgets = {
          'start_time': forms.TextInput(attrs={'size': 5, 'class': 'clock'}),
          'end_time': forms.TextInput(attrs={'size': 5, 'class': 'clock'}),
          'duration': forms.TextInput(attrs={'size': 5, 'class': 'clock'}),
          'note': forms.Textarea(attrs={'rows': 2, 'cols': 8}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")
        duration = cleaned_data.get("duration")
        if start_time and end_time:
            return cleaned_data
        elif not duration:
            self.add_error('duration', 'Required either duration or start_time and finish_time.')
        else:
            return cleaned_data


TimesheetTaskFormSet = inlineformset_factory(Timesheet, TimesheetTask, form=TimesheetTaskForm, extra=1)


class ProjectMembershipForm(ModelForm):
    class Meta:
        model = ProjectMembership
        exclude = ('created_at',)
        widgets = {
          'duration': forms.TextInput(attrs={'size': 10, 'class': 'clock', 'placeholder': 'HH:MM:SS'}),
        }

ProjectMembershipFormSet = inlineformset_factory(Project, ProjectMembership, form=ProjectMembershipForm, extra=1)


class SearchForm(forms.Form):
    resource_name = forms.CharField(label='Resource name', max_length=100)
    from_date = forms.DateField(initial=datetime.today().date())
    to_date = forms.DateField(initial=datetime.today().date())
