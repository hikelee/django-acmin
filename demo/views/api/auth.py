import json

from django.contrib.auth import authenticate, login, logout

from acmin.utils import json_response
from acmin.views import route


@route("api/demo/auth/logout/")
def logout_view(request):
    logout(request)
    return json_response(dict(status=0))


@route("api/demo/auth/login/")
def login_view(request):
    obj = json.loads(request.body)
    username = obj.get("username")
    password = obj.get("password")
    print(username, password)
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return json_response(dict(
            status=200,
            data=dict(
                title=user.title,
                avatar="https://gw.alipayobjects.com/zos/rmsportal/BiazfanxmamNRoxxVxka.png",
            )
        ))
    else:
        return json_response(dict(
            status=403,
            message="login failed"
        ))
