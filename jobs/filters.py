import django_filters
from django import forms
from .models import Job

class JobFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(
        method='custom_search',
        label="Search",
        widget=forms.TextInput(attrs={'placeholder': 'Job title, keyword, or company'})
    )
    location = django_filters.CharFilter(
        field_name='location',
        lookup_expr='icontains',
        label="Location",
        widget=forms.TextInput(attrs={'placeholder': 'e.g., New York, Remote'})
    )
    job_type = django_filters.ChoiceFilter(
        field_name='job_type',
        choices=Job.JOB_TYPE_CHOICES,
        empty_label="All Job Types",
        label="Job Type"
    )

    class Meta:
        model = Job
        fields = ['search', 'location', 'job_type']

    def custom_search(self, queryset, name, value):
        return queryset.filter(
            django_filters.Q(title__icontains=value) |
            django_filters.Q(description__icontains=value) |
            django_filters.Q(company__name__icontains=value)
        )
