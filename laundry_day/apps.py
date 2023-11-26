from django.apps import AppConfig


class LaundryDayConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'laundry_day'

    def ready(self):
        import laundry_day.signals
