from django.db import models
from django.conf import settings


class UserProfile(models.Model):
    USER_TYPE_CHOICES = [
        ('job_seeker', 'Job Seeker'),
        ('employer', 'Employer'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='job_seeker')
    phone_number = models.CharField(max_length=20, blank=True)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=200, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_user_type_display()}"

    @property
    def is_employer(self):
        return self.user_type == 'employer'

    @property
    def is_job_seeker(self):
        return self.user_type == 'job_seeker'


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


def save_user_profile(sender, instance, **kwargs):
    # Ensure profile exists before saving (for manual user creation in shells/tests)
    try:
        instance.profile.save()
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user=instance)