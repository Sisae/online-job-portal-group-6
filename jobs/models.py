from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone


class Job(models.Model):
    JOB_TYPE_CHOICES = [
        ('full-time', 'Full Time'),
        ('part-time', 'Part Time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
        ('temporary', 'Temporary'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField()
    company = models.ForeignKey('companies.Company', on_delete=models.CASCADE, related_name='jobs')
    location = models.CharField(max_length=200)
    remote = models.BooleanField(default=False)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default='full-time')
    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    posted_date = models.DateTimeField(auto_now_add=True)
    closing_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_jobs')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-posted_date']

    def __str__(self):
        return f"{self.title} at {self.company.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.title}-{self.company.name}")
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('jobs:job_detail', kwargs={'slug': self.slug})

    def is_open(self):
        return self.is_active and self.closing_date > timezone.now()

    def get_application_count(self):
        return self.applications.count()