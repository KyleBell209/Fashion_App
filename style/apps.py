from django.apps import AppConfig


class StyleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'style'

    def ready(self):
        import style.signals