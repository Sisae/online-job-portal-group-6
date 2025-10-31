from django import forms
from .models import Job


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'location', 'remote', 'job_type', 'salary', 'closing_date']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 6}),
            'closing_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'salary': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
        }


