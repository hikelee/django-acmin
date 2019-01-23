from inspect import isfunction

from django.http import HttpResponse

from acmin.router import route
from acmin.utils import *

methods = {}


def to_json(data, fields):
    if 'QuerySet' in str(type(data)):
        result = [to_json(obj, fields) for obj in data]
    else:
        result = {}
        for name in fields:
            field = name
            if "|" in name:
                parts = name.split("|")
                name = parts[1]
                field = parts[0] + ".id"
            result[name] = attrs.attr(data, field)
    return result


class RouteMeta(type):
    def __new__(mcs, name, bases, attrs):
        cls = type.__new__(mcs, name, bases, attrs)

        for key, value in attrs.items():
            if isfunction(value):
                u = attr(value, "url")
                if u:
                    app_name = cls.__module__.split(".")[0]
                    prefix = f'/{cls._function_name}/{app_name}/{cls.__module__.split(".").pop()}'
                    setattr(cls, key, route(u, prefix)(value))

        return cls


class AcminView(metaclass=RouteMeta):

    def context(self):
        return {}

    def render(self, template_name: str, context: dict = None):
        updated_context = self.context() or {}
        updated_context.update(context or {})
        name = template_name[1:] if template_name.startswith("/") else template_name
        return render(self.request, name, updated_context)

    @staticmethod
    def json_response(dict_instance: dict):
        return json_response(dict_instance)
        # return HttpResponse(json.dumps(dict_instance, cls=CJsonEncoder), content_type="application/json")

    @classmethod
    def text_response(cls, text: str):
        return HttpResponse(text, content_type="text/html")

    @classmethod
    def error_json_message(cls, message: str = None):
        return cls.json_response({"status": 1, "message": message})

    @classmethod
    def ok_json_message(cls, message: str = None):
        return cls.json_response({"status": 0, "message": message})

    @classmethod
    def ok_data(cls, data=None):
        obj = {"status": 0}
        if data:
            obj['data'] = data
        return cls.json_response(obj)

    def int_param(self, param_name, default=0) -> int:
        return int_param(self.request, param_name, default)

    def bool_param(self, param_name, default=False) -> bool:
        return bool_param(self.request, param_name, default)

    def param(self, key, default=None) -> str:
        return param(self.request, key, default)

    def mac(self):
        return (self.param("mac", "") or self.param("imei", "")).upper()


class ApiView(AcminView):
    _function_name = "api"


class WebView(AcminView):
    _function_name = "web"


def url(param=None):
    if isfunction(param):
        param.url = "/" + param.__name__
        return get_wrapper(param)
    else:
        def decorate(func):
            if param is None:
                path = func.__name__
            else:
                path = param[1:] if param and param.startswith("/") else param
            func.url = "/" + path
            return get_wrapper(func)

        return decorate
