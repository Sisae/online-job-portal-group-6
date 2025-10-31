from django.contrib import admin
from .models import Job


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'location', 'job_type', 'is_active', 'posted_date', 'closing_date']
    list_filter = ['job_type', 'is_active', 'remote', 'posted_date', 'closing_date']
    search_fields = ['title', 'description', 'company__name', 'location']
    readonly_fields = ['slug', 'created_at', 'updated_at']
    raw_id_fields = ['company', 'created_by']
    prepopulated_fields = {'slug': ('title',)}