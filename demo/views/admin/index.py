import random
import string

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader

from acmin.models import ContentType, Permission, PermissionItem
from acmin.utils import attr, import_model


def get_nodes(user):
    nodes = [
        ("基础信息", [import_model("acmin", ct.name) for ct in ContentType.objects.filter(app="acmin")]),
        ("业务信息", [import_model("demo", ct.name) for ct in ContentType.objects.filter(app="demo")]),
    ]
    result = []
    for name, models in nodes:
        sub = [(model.__name__, attr(model, "_meta.verbose_name")) for model in models if
               Permission.has_permission(user, model, PermissionItem.listable)]
        if sub:
            result.append((name, sub))
    return result


@login_required
def index(request):
    context = {
        "random": ''.join(random.sample(string.ascii_letters + string.digits, 8)),
        "nodes": get_nodes(request.user),
        "site_name": "acmin demo",
        "copyright": "acmin © 2016-2018",
        "role_name": "",

    }
    return HttpResponse(loader.get_template('admin/main.html').render(context, request))
