from django.apps import AppConfig as DjangoAppConfig


class AppConfig(DjangoAppConfig):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    name = 'demo'

    def ready(self):
        pass
        # if 'runserver' in sys.argv:
