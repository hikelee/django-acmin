from functools import partial

import django.apps
from django.conf import settings
from django.conf.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from acmin.forms import LoginForm
from acmin.utils import attr
from acmin.views import get_urlpatterns
from acmin.views.admin import get_view
from acmin.views.admin import user
from demo.views import rest
from demo.views.admin import index as main_index

app_name = __name__.split(".")[0]

models = [model for model in django.apps.apps.get_models() if
          model.__module__.startswith(app_name) or model.__module__.startswith("acmin")]


def get_manual_patterns():
    urlpatterns = []
    admin_prefix = attr(settings, 'ACMIN_ADMIN_PREFIX')
    for model in models:
        name = model.__name__
        prefix = f'{admin_prefix}/{app_name}/{name}'
        view = partial(get_view, model)
        urlpatterns += [
            path(f'{prefix}/', view("list"), name=f'{name}-list'),
            path(f'{prefix}/export/', view("export"), name=f'{name}-export'),
            path(f'{prefix}/create/', view("create"), name=f'{name}-create'),
            path(f'{prefix}/<int:pk>/', view("update"), name=f'{name}-update'),
            path(f'{prefix}/<int:pk>/delete/', view("delete"), name=f'{name}-delete'),
        ]

    urlpatterns += [
        path(f'{admin_prefix}/{app_name}/user/login/', user.LoginView.as_view(success_url='/'), kwargs={'authentication_form': LoginForm}),
        path(f'{admin_prefix}/{app_name}/', main_index),

    ]

    return urlpatterns


def get_patterns():
    router = DefaultRouter()
    router.register(r'members', rest.MemberViewSet)
    router.register(r'fields', rest.FieldViewSet)

    admin_patterns = get_manual_patterns()
    auto_patterns = get_urlpatterns()
    rest_patterns = [
        path(f'api/{app_name}/', include(router.urls)),
    ]

    return admin_patterns + auto_patterns + rest_patterns
