import random
import string

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader

from acmin import models as acmin_models
from acmin.utils import attr
from demo.models import *

nodes = [
    ("基础信息",
     [acmin_models.Group, acmin_models.User, acmin_models.KeyValue, acmin_models.Model, acmin_models.GroupFilter,
      acmin_models.UserFilter, acmin_models.GroupPermission, acmin_models.UserPermission]),
    ("业务信息", [Platform, ClickFarming, Expenditure, Province, City, Area, Address, Member, Author, Book, Order]),
]


def get_listable_models(user):
    listable_models = list(acmin_models.Model.objects.filter(
        grouppermission__group__user=user,
        grouppermission__enabled=True,
        grouppermission__listable=True
    )) + list(acmin_models.Model.objects.filter(
        userpermission__user=user,
        grouppermission__enabled=True,
        grouppermission__listable=True
    ))
    return set([model.name for model in listable_models])


def get_nodes(user):
    listable_models = get_listable_models(user)
    result = []
    for name, models in nodes:
        sub = [(model.__name__, attr(model, "_meta.verbose_name")) for model in models if
               model.__name__ in listable_models or acmin_models.SuperPermissionModel.__name__ in listable_models]
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
