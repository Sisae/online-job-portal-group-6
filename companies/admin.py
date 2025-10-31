from django.contrib import admin
from .models import Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'contact_email', 'owner', 'created_at']
    list_filter = ['created_at', 'location']
    search_fields = ['name', 'description', 'location']
    readonly_fields = ['created_at', 'updated_at']
    raw_id_fields = ['owner']