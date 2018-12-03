from acmin.utils import attr


def init_models(sender, **kwargs):
    import django.apps
    from acmin.models import AcminContentType, AcminModel
    app_models = {m.__name__: attr(m, '_meta.verbose_name') for m in django.apps.apps.get_models() if issubclass(m, AcminModel)}
    db_models = {m.name: m for m in AcminContentType.objects.all()}
    for name, verbose_name in app_models.items():
        model = db_models.get(name)
        if model:
            if model.verbose_name != verbose_name:
                model.verbose_name = verbose_name
                model.save()
        else:
            AcminContentType.objects.create(name=name, verbose_name=verbose_name)

    for name, model in db_models.items():
        if name not in app_models:
            model.delete()
