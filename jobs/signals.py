from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import UserProfile
from core.services.notification_service import send_templated_email
from jobs.models import Job


@receiver(post_save, sender=Job)
def notify_on_new_job(sender, instance: Job, created: bool, **kwargs):
    if not created:
        return

    # Find job seekers with an email
    seekers = UserProfile.objects.select_related('user').filter(user_type='job_seeker')
    recipient_emails = [p.user.email for p in seekers if getattr(p.user, 'email', None)]
    if not recipient_emails:
        return

    context = {
        'job': instance,
        'company': instance.company,
    }
    send_templated_email(
        subject=f"New job posted: {instance.title} at {instance.company.name}",
        template_name='emails/job_new_alert.txt',
        context=context,
        recipients=recipient_emails,
    )


