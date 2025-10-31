from django.db.models.signals import pre_save
from django.dispatch import receiver

from applications.models import Application
from core.services.notification_service import send_templated_email


@receiver(pre_save, sender=Application)
def notify_on_application_status_change(sender, instance: Application, **kwargs):
    if not instance.pk:
        return
    try:
        previous = Application.objects.get(pk=instance.pk)
    except Application.DoesNotExist:
        return
    if previous.status == instance.status:
        return

    applicant_email = getattr(instance.applicant, 'email', None)
    if not applicant_email:
        return

    context = {
        'applicant': instance.applicant,
        'job': instance.job,
        'old_status': previous.get_status_display(),
        'new_status': instance.get_status_display(),
        'application': instance,
    }
    send_templated_email(
        subject=f"Your application status updated: {instance.get_status_display()}",
        template_name='emails/application_status_update.txt',
        context=context,
        recipients=[applicant_email],
    )


