import datetime

from django import forms
from django.forms import ModelForm
from django.forms.models import inlineformset_factory

from tracker.models import *


class EmployeeDocumentForm(ModelForm):
    class Meta:
        model = EmployeeDocument
        exclude = ('created_at',)
        widgets = {
          'description': forms.Textarea(attrs={'rows': 2, 'cols': 8}),
        }

class EmployeeExpenseForm(ModelForm):
    class Meta:
        model = EmployeeExpense
        exclude = ('created_at', 'status',)


class ProjectExpenseForm(ModelForm):
    class Meta:
        model = ProjectExpense
        exclude = ('created_at', 'status',)


class VendorExpenseForm(ModelForm):
    class Meta:
        model = VendorExpense
        exclude = ('created_at', 'status',)


class TimesheetForm(ModelForm):

    class Meta:
        model = Timesheet
        exclude = ('created_at',)

    def clean(self):
        cleaned_data = super().clean()
        sign_in = cleaned_data.get("sign_in")
        sign_out = cleaned_data.get("sign_out")
        if sign_in > sign_out:
            msg = u"Sign out should be greater than sign in."
            self.add_error('sign_out', msg)
            # self._errors["sign_out"] = self.error_class([msg])


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


class ProjectDocumentForm(ModelForm):
    class Meta:
        model = ProjectDocument
        exclude = ('created_at',)
        widgets = {
          'description': forms.Textarea(attrs={'rows': 2, 'cols': 8}),
        }


class VendorDocumentForm(ModelForm):
    class Meta:
        model = VendorDocument
        exclude = ('created_at',)
        widgets = {
          'description': forms.Textarea(attrs={'rows': 2, 'cols': 8}),
        }


class SearchForm(forms.Form):
    resource_name = forms.CharField(label='Resource name', max_length=100,\
                                        widget = forms.TextInput(attrs={'placeholder': 'FirstName  LastName'}))
    from_date = forms.DateField(initial=datetime.today().date(), widget=forms.widgets.DateInput(format="%m/%d/%Y"))
    to_date = forms.DateField(initial=datetime.today().date(), widget=forms.widgets.DateInput(format="%m/%d/%Y"))


class DurationSearchForm(forms.Form):
    from_date = forms.DateField(initial=datetime.today().date(), widget=forms.widgets.DateInput(format="%m/%d/%Y"))
    to_date = forms.DateField(initial=datetime.today().date(), widget=forms.widgets.DateInput(format="%m/%d/%Y"))


class InvoiceItemForm(ModelForm):
    class Meta:
        model = InvoiceItem
        exclude = ('created_at',)
        widgets = {
          'description': forms.Textarea(attrs={'rows': 1, 'cols': 8}),
          'pay_rate': forms.TextInput(attrs={'class': 'pay_rate'}),
          'quantity': forms.TextInput(attrs={'class': 'quantity'}),
          'amount': forms.TextInput(attrs={'class': 'amount'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        pay_rate = cleaned_data.get("pay_rate")
        quantity = cleaned_data.get("quantity")
        amount = cleaned_data.get("amount")
        if pay_rate and quantity:
            return cleaned_data
        elif not amount:
            self.add_error('amount', 'Required either amount or rate and quatity.')
        else:
            return cleaned_data


InvoiceItemFormSet = inlineformset_factory(Invoice, InvoiceItem, form=InvoiceItemForm, extra=1)
