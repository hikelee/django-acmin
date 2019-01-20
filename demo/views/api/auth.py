import json

from django.contrib.auth import authenticate, login, logout

from acmin.views import api_route


@api_route("api/demo/auth/logout/")
def logout_view(request):
    logout(request)
    return dict(status=200)


@api_route("api/demo/auth/login/", login_required=False)
def login_view(request):
    obj = json.loads(request.body)
    username = obj.get("username")
    password = obj.get("password")
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return dict(
            status=200,
            data=dict(
                title=user.title,
                avatar="https://gw.alipayobjects.com/zos/rmsportal/BiazfanxmamNRoxxVxka.png",
            ))
    else:
        return dict(status=403, message="login failed")
