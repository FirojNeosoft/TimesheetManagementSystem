from django.contrib import admin
from tenants.models import *

# Register your models here.


class CompanyAdmin(admin.ModelAdmin):
    model = Company
    list_display = ['name', 'schema_name', 'domain_url']

admin.site.register(Company, CompanyAdmin)