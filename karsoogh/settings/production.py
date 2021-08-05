from karsoogh.settings.settings_base import *

DEBUG = os.environ.get("DEBUGGING") == "DEBUG"

ALLOWED_HOSTS = os.environ.get('HOST', "").split(",")

SECRET_KEY = os.environ.get(
    'SECRET_KEY', '3s%v6jaceszv$rabw)fj85+_alf^+v8ryanaf2qa&^n1)-3+x&')

DB_NAME = os.environ.get('DB_NAME', "")
DB_USER = os.environ.get('DB_USER', "")
DB_PASS = os.environ.get('DB_PASS', "")
DB_HOST = os.environ.get('DB_HOST', "")
DB_PORT = os.environ.get('DB_PORT', "")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'Interkarsolar',
        'USER': 'Admin',
        'PASSWORD': '147456admin',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=14),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': False,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUTH_HEADER_TYPES': ('JWT',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
}