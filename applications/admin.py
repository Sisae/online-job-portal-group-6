from django.contrib import admin
from .models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['applicant', 'job', 'status', 'applied_date']
    list_filter = ['status', 'applied_date', 'job__company']
    search_fields = ['applicant__first_name', 'applicant__last_name', 'job__title', 'job__company__name']
    readonly_fields = ['applied_date', 'updated_at']
    raw_id_fields = ['job', 'applicant']