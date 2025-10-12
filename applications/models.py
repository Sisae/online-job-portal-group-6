from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone


class Application(models.Model):
    STATUS_CHOICES = [
        ('applied', 'Applied'),
        ('under_review', 'Under Review'),
        ('interview', 'Interview'),
        ('offer', 'Offer'),
        ('rejected', 'Rejected'),
    ]

    job = models.ForeignKey('jobs.Job', on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='applications')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied')
    cover_letter = models.TextField(blank=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    applied_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True, help_text="Internal notes for employer")

    class Meta:
        unique_together = ['job', 'applicant']
        ordering = ['-applied_date']

    def __str__(self):
        return f"{self.applicant.get_full_name()} - {self.job.title}"

    def get_absolute_url(self):
        return reverse('applications:application_detail', kwargs={'pk': self.pk})

    def get_status_display_class(self):
        status_classes = {
            'applied': 'primary',
            'under_review': 'info',
            'interview': 'warning',
            'offer': 'success',
            'rejected': 'danger',
        }
        return status_classes.get(self.status, 'secondary')