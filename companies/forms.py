from django import forms
from .models import Company


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'website', 'description', 'logo', 'location', 'contact_email']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'website': forms.URLInput(attrs={'placeholder': 'https://example.com'}),
        }


