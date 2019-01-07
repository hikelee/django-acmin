from acmin.utils import json_response
from acmin.views import route

breadcrumb_data = {
    '/generic/list/': {
        'path': '/generic/list/',
        'name': '通用列表',
        'exact': True,
        'locale': 'menu.generic.glist',
    },
    '/generic': {
        'path': '/generic',
        'icon': 'table',
        'name': '通用',
        'locale': 'menu.generic',
        'authority': [
            'admin',
            'user',
        ],
        'children': [
            {
                'path': '/generic/list/',
                'name': '通用列表',
                'exact': True,
                'locale': 'menu.generic.glist',
            },
        ],
    },
    '/exception/403': {
        'path': '/exception/403',
        'name': '403',
        'exact': True,
        'locale': 'menu.exception.not-permission',
    },
    '/exception/404': {
        'path': '/exception/404',
        'name': '404',
        'exact': True,
        'locale': 'menu.exception.not-find',
    },
    '/exception/500': {
        'path': '/exception/500',
        'name': '500',
        'exact': True,
        'locale': 'menu.exception.server-error',
    },
    '/exception': {
        'name': '异常页',
        'icon': 'warning',
        'path': '/exception',
        'locale': 'menu.exception',
        'authority': [
            'admin',
            'user',
        ],
        'children': [
            {
                'path': '/exception/403',
                'name': '403',
                'exact': True,
                'locale': 'menu.exception.not-permission',
            },
            {
                'path': '/exception/404',
                'name': '404',
                'exact': True,
                'locale': 'menu.exception.not-find',
            },
            {
                'path': '/exception/500',
                'name': '500',
                'exact': True,
                'locale': 'menu.exception.server-error',
            },
        ],
    },
    '/account/center': {
        'path': '/account/center',
        'name': '个人中心',
        'locale': 'menu.account.center',
        'children': [],
    },
    '/account/settings': {
        'path': '/account/settings',
        'name': '个人设置',
        'locale': 'menu.account.settings',
        'children': [],
    },
    '/account': {
        'name': '个人页',
        'icon': 'user',
        'path': '/account',
        'locale': 'menu.account',
        'authority': [
            'admin',
            'user',
        ],
        'children': [
            {
                'path': '/account/center',
                'name': '个人中心',
                'locale': 'menu.account.center',
                'children': [],
            },
            {
                'path': '/account/settings',
                'name': '个人设置',
                'locale': 'menu.account.settings',
                'children': [],
            },
        ],
    },
};

menu_data = [
    {
        'path': '/generic',
        'icon': 'table',
        'name': '通用',
        'locale': 'menu.generic',
        'authority': [
            'admin',
            'user',
        ],
        'children': [
            {
                'path': '/generic/list/',
                'name': '通用列表',
                'exact': True,
                'locale': 'menu.generic.glist',
            },
        ],
    },
    {
        'name': '异常页',
        'icon': 'warning',
        'path': '/exception',
        'locale': 'menu.exception',
        'authority': [
            'admin',
            'user',
        ],
        'children': [
            {
                'path': '/exception/403',
                'name': '403',
                'exact': True,
                'locale': 'menu.exception.not-permission',
            },
            {
                'path': '/exception/404',
                'name': '404',
                'exact': True,
                'locale': 'menu.exception.not-find',
            },
            {
                'path': '/exception/500',
                'name': '500',
                'exact': True,
                'locale': 'menu.exception.server-error',
            },
        ],
    },
    {
        'name': '个人页',
        'icon': 'user',
        'path': '/account',
        'locale': 'menu.account',
        'authority': [
            'admin',
            'user',
        ],
        'children': [
            {
                'path': '/account/center',
                'name': '个人中心',
                'locale': 'menu.account.center',
                'children': [],
            },
            {
                'path': '/account/settings',
                'name': '个人设置',
                'locale': 'menu.account.settings',
                'children': [],
            },
        ],
    },
]


# http://127.0.0.1:8000/api/demo/menu/
@route("api/demo/menu/")
def get(request):
    return json_response(dict(menu=menu_data, breadcrumb=breadcrumb_data), safe=False)
