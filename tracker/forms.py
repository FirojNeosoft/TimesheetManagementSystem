from django import forms
from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from django.forms import formset_factory

from tracker.models import *


class TimesheetTaskForm(ModelForm):
    class Meta:
        model = TimesheetTask
        exclude = ('created_at',)
        widgets = {
          'start_time': forms.TextInput(attrs={'size': 5, 'class': 'clock'}),
          'end_time': forms.TextInput(attrs={'size': 5, 'class': 'clock'}),
          'note': forms.Textarea(attrs={'rows': 2, 'cols': 8}),
        }

TimesheetTaskFormSet = inlineformset_factory(Timesheet, TimesheetTask,
                                            form=TimesheetTaskForm, extra=1)