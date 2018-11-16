import random
import string

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader

from acmin.models import import_model
from acmin.utils import attr

app_name = __name__.split(".")[0]
full_nodes = [
    ("基础信息", ["User", "Province", "City", "Area", "Address", "Member", "Author", "Book", "Order"]),
]


def get_nodes(user):
    def to_tuple(node):
        if not isinstance(node, tuple):
            model = import_model(app_name, node)
            node = (node, attr(model, '_meta.verbose_name'))
        return node

    result = []
    for (name, nodes) in full_nodes:
        nodes = [to_tuple(node) for node in nodes]
        nodes = [node[0:2] for node in nodes]
        if nodes:
            result.append((name, nodes))
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
