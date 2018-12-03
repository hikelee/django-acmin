from acmin.utils import attr


def init_models(sender, **kwargs):
    import django.apps
    from acmin.models import ContentType, AcminModel
    app_models = {m.__name__: attr(m, '_meta.verbose_name') for m in django.apps.apps.get_models() if issubclass(m, AcminModel)}
    contenttypes = {m.name: m for m in ContentType.objects.all()}
    for name, verbose_name in app_models.items():
        contenttype = contenttypes.get(name)
        if contenttype:
            if contenttype.verbose_name != verbose_name:
                contenttype.verbose_name = verbose_name
                contenttype.save()
        else:
            ContentType.objects.create(name=name, verbose_name=verbose_name)

    for name, contenttype in contenttypes.items():
        if name not in app_models:
            contenttype.delete()
