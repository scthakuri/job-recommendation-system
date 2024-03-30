from django.contrib import admin
from job.models import *

# Register your models here.
class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'skills_required', 'expiry_date']

    class Meta:
        proxy = True
        verbose_name_plural = "Job"
        verbose_name = "Jobs"

class CompanyAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'industry', 'location']

    class Meta:
        proxy = True
        verbose_name_plural = "Company"
        verbose_name = "Companies"

admin.site.register(Job, JobAdmin)
admin.site.register(Company, CompanyAdmin)