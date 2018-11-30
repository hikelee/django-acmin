def init_models(sender, **kwargs):
    from django.conf import settings
    import django.apps
    from acmin.models import Model
    app_name = settings.APP_NAME
    app_models = {m.__name__: m._meta.verbose_name for m in django.apps.apps.get_models() if m.__module__.startswith(app_name)}
    db_models = {m.name: m for m in Model.objects.all()}
    for name, verbose_name in app_models.items():
        model = db_models.get(name)
        if model:
            if model.verbose_name != verbose_name:
                model.verbose_name = verbose_name
                model.save()
        else:
            Model.objects.create(name=name, verbose_name=verbose_name)

    for name, model in db_models.items():
        if name not in app_models:
            model.delete()
