from django.contrib.auth import authenticate, login, logout

from acmin.utils import param, json_response
from acmin.views import route


@route("api/demo/user/logout")
def logout_view(request):
    logout(request)
    return json_response(dict(status=0))


@route("api/demo/user/login")
def login(request):
    user = authenticate(request, username=param(request, "username"), password=param(request, "password"))
    if user is not None:
        login(request, user)
        return json_response(dict(status=0))
    else:
        return json_response(dict(status=1))
