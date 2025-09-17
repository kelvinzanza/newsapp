from django.apps import AppConfig


class ArchiveConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'archive'

    def ready(self):
        '''
        Connects the app's signals when the app is ready.
        '''
        super().ready()

