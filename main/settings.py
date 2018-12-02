import os
import socket
import time

from acmin.utils import get_ip, is_windows

IS_PRODUCTION = socket.gethostname() in ['jn1', 'public']
DEBUG = not IS_PRODUCTION
# DEBUG = False
ACMIN_ADMIN_PREFIX = ADMIN_PREFIX = "backend"
ACMIN_APP_NAME = APP_NAME = 'demo'
ACMIN_SHOW_SQL = False
ACMIN_ENABLE_CACHE = True
ACMIN_FUNCTION_NAME = "acmin-demo"

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SECRET_KEY = 'cc25adry^l0r87l+228xxxa^%67q015z7j9^uc96jm=bbb0e^l'
ALLOWED_HOSTS = ["*"]
ROOT_URLCONF = 'main.urls'
WSGI_APPLICATION = 'main.wsgi.application'
LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_L10N = True
USE_TZ = False
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
DATE_TIME_FORMAT = '%Y-%m-%d'
PAGINATE_BY = 10
START_TIME = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

AUTH_USER_MODEL = f'acmin.User'
LOGIN_URL = f'/{ADMIN_PREFIX}/{APP_NAME}/user/login/'
INDEX_URL = f'/{ADMIN_PREFIX}/{APP_NAME}/'
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'acmin.middlewares.LogMiddleware',
]
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 'DIRS': [BASE_DIR.child('admin')],
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.static',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'acmin.processors.extra_context',
                'demo.processors.extra_context'
            ],
        },
    },
]


def rotating_handler(name):
    return {
        'level': 'DEBUG',
        'filters': ['f1'],
        'formatter': 'simple',
        'class': 'logging.handlers.TimedRotatingFileHandler',
        'when': 'midnight',
        'interval': 1,
        'backupCount': 100,
        'filename': f'/var/log/{APP_NAME}/{name}.log',
    }


LOG_FOLDER = f'/var/log/{APP_NAME}'


def file_handler(name):
    return {
        'level': 'DEBUG',
        'filters': ['f1'],
        'formatter': 'simple',
        'class': 'logging.FileHandler',
        'filename': f'{LOG_FOLDER}/{name}.log',
    }


def console_handler():
    return {'level': 'DEBUG', 'filters': ['f1'], 'formatter': 'simple', 'class': 'logging.StreamHandler', }


def get_log_setting(debug):
    log_modules = [APP_NAME, "acmin"]
    return {
        'version': 1,
        'disable_existing_loggers': True,
        'filters': {'f1': {'()': 'django.utils.log.RequireDebug' + str(debug)}},
        'formatters': {'simple': {'format': '%(levelname)s %(asctime)s %(message)s'}, },
        'handlers': dict({key: file_handler(key) for key in log_modules}, **{'console': console_handler()}),
        'loggers': {key: {'level': 'INFO', 'handlers': ['console', key]} for key in log_modules}
    }


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'acmin',
    APP_NAME
]

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]

CACHALOT_UNCACHABLE_TABLES = (
    'django_migrations',

)

MEDIA_ROOT = "/var/www/media/" if is_windows() else "/var/www/media/"

MEDIA_URL = f'http://{get_ip()}/media/'

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    f"{BASE_DIR}/static"
]

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

SQLITE_DATABASE = {'default': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': F"{BASE_DIR}/1.db",
    'TEST_NAME': F"{BASE_DIR}/1-test.db",
}}

DATABASES = SQLITE_DATABASE

LOGGING = get_log_setting(DEBUG)

for folder in [LOG_FOLDER, MEDIA_ROOT]:
    os.makedirs(folder, exist_ok=True)
