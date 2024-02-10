from django.apps import AppConfig


class PredictsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'predicts'

    #this is overwrite function to work with django-apschedule
    def ready(self):
        from jobs import updater
        updater.start()
