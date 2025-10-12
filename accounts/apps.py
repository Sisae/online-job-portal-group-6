from django.apps import AppConfig
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        # Connect signals to the actual user model to support swappable AUTH_USER_MODEL
        from .models import create_user_profile, save_user_profile
        UserModel = get_user_model()
        post_save.connect(create_user_profile, sender=UserModel, dispatch_uid='accounts_create_user_profile')
        post_save.connect(save_user_profile, sender=UserModel, dispatch_uid='accounts_save_user_profile')
