from functools import partial

import django.apps
from django.conf import settings
from django.urls import path

from acmin.utils import attr
from acmin.views import get_urlpatterns
from acmin.views.admin import get_view
from acmin.views.admin import user
from demo.forms.user import LoginForm
from demo.views.admin import index as main_index

app_name = __name__.split(".")[0]

models = [model for model in django.apps.apps.get_models() if
          model.__module__.startswith(app_name) or model.__module__.startswith("acmin")]


def get_patterns():
    urlpatterns = get_urlpatterns()
    admin_prefix = attr(settings, 'ADMIN_PREFIX')
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

# if "runserver" in sys.argv:
#    from .utils.decorators import task
#    @task(start=10, interval=60)
#    def show_trace():
#        from .utils import profile
#        profile.show_trace()
#    show_trace()
