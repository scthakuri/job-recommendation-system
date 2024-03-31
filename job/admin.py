from django.contrib import admin
from job.models import *

# Register your models here.
class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'skills_required', 'expiry_date']

    class Meta:
        proxy = True
        verbose_name_plural = "Jobs"
        verbose_name = "Job"

class CompanyAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'industry', 'location']

    class Meta:
        proxy = True
        verbose_name_plural = "Companies"
        verbose_name = "Company"

class UserInteractionAdmin(admin.ModelAdmin):
    list_display = ['job', 'user', 'timestamp']

    class Meta:
        proxy = True
        verbose_name_plural = "Applications"
        verbose_name = "Application"


admin.site.register(Job, JobAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(UserInteraction, UserInteractionAdmin)