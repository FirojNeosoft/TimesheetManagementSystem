from django.contrib import admin

from tracker.models import *


class ProjectActivityAdmin(admin.ModelAdmin):
    list_display = ('name',)


class TimesheetTaskInline(admin.TabularInline):
    model = TimesheetTask


class TimesheetAdmin(admin.ModelAdmin):
    model = Timesheet
    inlines = [TimesheetTaskInline,]
    # add_form_template = 'timesheet_form.html'
    # change_form_template = 'timesheet_form.html'


class ExpenseTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'status')

admin.site.register(ProjectActivity, ProjectActivityAdmin)
admin.site.register(Timesheet, TimesheetAdmin)
admin.site.register(ExpenseType, ExpenseTypeAdmin)
