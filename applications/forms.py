from django import forms
from .models import Application


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['cover_letter', 'resume']
        widgets = {
            'cover_letter': forms.Textarea(attrs={'rows': 6, 'placeholder': 'Write your cover letter here...'}),
        }


class ApplicationStatusForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['status', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add internal notes about this application...'}),
        }


