import random
import string

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader

from acmin.models import ContentType, Permission, PermissionItem
from acmin.utils import attr, import_model


def get_nodes(user):
    default_node = ""
    nodes = [
        ("基础信息", [import_model("acmin", ct.name) for ct in ContentType.objects.filter(app="acmin")]),
        ("业务信息", [import_model("demo", ct.name) for ct in ContentType.objects.filter(app="demo")]),
    ]
    result = []
    for title, models in nodes:
        leaves = []
        for model in models:
            if Permission.has_permission(user, model, PermissionItem.listable):
                class_name = model.__name__
                leaves.append((class_name, attr(model, "_meta.verbose_name")))
                if not default_node:
                    default_node = class_name
        if leaves:
            result.append((title, leaves))
    return result, default_node


@login_required
def index(request):
    import django.apps
    from acmin.utils import attr
    for model in django.apps.apps.get_models():
        for field in attr(model, '_meta.fields'):
            print(vars(field))
    nodes, default_node = get_nodes(request.user)
    context = {
        "random": ''.join(random.sample(string.ascii_letters + string.digits, 8)),
        "nodes": nodes,
        "site_name": "acmin demo",
        "copyright": "acmin © 2016-2018",
        "role_name": "",
        "default_node": default_node

    }
    return HttpResponse(loader.get_template('admin/main.html').render(context, request))
