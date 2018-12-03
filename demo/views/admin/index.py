import random
import string

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader

from acmin.models import *
from acmin.utils import attr
from demo.models import *

nodes = [
    ("基础信息",
     [Group, User, KeyValue, AcminContentType, GroupFilter, UserFilter, GroupPermission, UserPermission]),
    ("业务信息", [Platform, ClickFarming, Expenditure, Province, City, Area, Address, Member, Author, Book, Order]),
]


def get_nodes(user):
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
