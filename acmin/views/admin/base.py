import logging

from django.conf import settings

from acmin.forms import load_form
from acmin.utils import attrs, memorize, import_class

logger = logging.getLogger(__name__)


@memorize
def get_base_view_class(app_name, action):
    return import_class(f"{app_name}.views.Base{action.capitalize()}View")


def get_view(model, action):
    app_name = settings.APP_NAME
    view_name = "%s%sView" % (model.__name__, action.capitalize())
    view = None
    try:
        view = import_class('%s.views.%s' % (app_name, view_name))
    except Exception:
        try:
            view = type("Dynamic%s" % view_name, (get_base_view_class(app_name, action),), dict(
                model=model,
                __module__=f'{app_name}.{__name__}',

            ))
        except Exception as e:
            logger.error(e)

    if view and attrs.attr(view, 'form_class', None) is None:
        setattr(view, "form_class", load_form(app_name, view.model))

    return view.as_view()
