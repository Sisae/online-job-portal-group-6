from django.apps import AppConfig


class ApplicationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'applications'
<<<<<<< HEAD

    def ready(self):
        # Import signal handlers
        from . import signals  # noqa: F401
=======
>>>>>>> 9030b895aaba431233f2d86f86d53ffd5681c3fa
