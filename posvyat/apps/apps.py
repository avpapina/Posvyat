from django.apps import AppConfig
from django.conf import settings


class MyappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps'

    def ready(self):
        if settings.SCHEDULER_AUTOSTART:
            from apps.google import start_scheduler
            start_scheduler()

