import json

from django.contrib.auth import authenticate, login, logout

from acmin.router import api_route


@api_route("api/demo/auth/logout/")
def logout_view(request):
    logout(request)
    return dict(status=200)


@api_route("api/demo/auth/userInfo/")
def user_info(request):
    user = request.user
    if user is not None:
        return {
            "status": 200,
            "data": {
                "name": "ROOT",
                "avatar": "https://gw.alipayobjects.com/zos/rmsportal/BiazfanxmamNRoxxVxka.png",
                "unreadCount": 11,
                "email": "antdesign@alipay.com",
                "signature": "海纳百川，有容乃大",
                "title": "交互专家",
                "group": "蚂蚁金服－某某某事业群－某某平台部－某某技术部－UED",
                "tags": [
                    {"key": "0", "label": "很有想法的"},
                    {"key": "1", "label": "专注设计"},
                    {"key": "2", "label": "辣~"},
                    {"key": "3", "label": "大长腿"},
                    {"key": "4", "label": "川妹子"},
                    {"key": "5", "label": "海纳百川"}
                ]
            },
            "message": "success"
        }
    else:
        return dict(status=403, message="login failed")


@api_route("api/demo/auth/login/", login_required=False)
def login_view(request):
    obj = json.loads(request.body)
    username = obj.get("username")
    password = obj.get("password")
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return dict(status=200)
    else:
        return dict(status=403, message="login failed")
