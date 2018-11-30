from django.apps import AppConfig
from django.db.models.signals import post_migrate

from acmin.management import init_models


class AcminConfig(AppConfig):
    name = 'acmin'

    def ready(self):
        from acmin import sql
        from acmin import cache
        post_migrate.connect(init_models)
        sql.patch()
        cache.patch()
