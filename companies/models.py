from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Company(models.Model):
    name = models.CharField(max_length=200)
    website = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    location = models.CharField(max_length=200)
    contact_email = models.EmailField()
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='company')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Companies'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('companies:company_detail', kwargs={'pk': self.pk})