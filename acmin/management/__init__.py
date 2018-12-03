def init_models(sender, **kwargs):
    import django.apps
    from acmin.models import ContentType, AcminModel
    contenttypes = {}
    for contenttype in ContentType.objects.all():
        contenttypes[contenttype.app + "-" + contenttype.name] = contenttype
    models = {}
    for model in [model for model in django.apps.apps.get_models() if issubclass(model, AcminModel)]:
        app = model.__module__.split(".")[0]
        name = model.__name__
        models[app + "-" + name] = model._meta.verbose_name

    for flag, verbose_name in models.items():
        contenttype = contenttypes.get(flag)
        if contenttype:
            if contenttype.verbose_name != verbose_name:
                contenttype.verbose_name = verbose_name
                contenttype.save()
        else:
            app, name = flag.split("-")
            ContentType.objects.create(app=app, name=name, verbose_name=verbose_name)

    for flag, contenttype in contenttypes.items():
        if flag not in models:
            contenttype.delete()
