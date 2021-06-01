"""
Django settings for karsoogh project.

Generated by 'django-admin startproject' using Django 3.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


def rel(x):
    return Path.joinpath(BASE_DIR, x)


def rel_media(x):
    return os.path.join(MEDIA_ROOT, x)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '3s%v6jaceszv$rabw)fj85+_alf^+v8ryanaf2qa&^n1)-3+x&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = [
    'http://localhost:80',
    'http://localhost:3000',
    'http://localhost:8000',
    'http://127.0.0.1:8000',
    'https://interkarsolar.ir',
    'http://185.239.105.157:8000',
]

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'accept-language',
    'cache-control',
    'authorization',
    'content-type',
    'content-length',
    'dnt',
    'origin',
    'pragma',
    'referer',
    'sec-ch-ua',
    'sec-ch-ua-mobile',
    'sec-fetch-dest',
    'sec-fetch-mode',
    'sec-fetch-site',
    'sec-fetch-user',
    'upgrade-insecure-requests',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'x-www-form-urlencoded',
    'token',
    'city',
    'province',
]

RESPONSE_TEMPLATE = '{{ "res_code": {}, "message": "{}", "data": {} }}'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Api.apps.ApiConfig',
    'Formula0.apps.Formula0Config',
    'corsheaders',
    # 'rest_framework',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'karsoogh.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'karsoogh.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'Karsoogh',
        'USER': 'Admin',
        'PASSWORD': '147456admin',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': str(os.path.join(BASE_DIR, "db.sqlite3")),
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Iran'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_ROOT = rel('static')

STATIC_URL = '/static/'

MEDIA_ROOT = rel('media')

MEDIA_URL = '/media/'

# payment properties:
API_TOKEN = '19e8961b-ad5a-4a65-807a-087c777f6e1b'
SANDBOX = '0'

GRADE = (
    (6, 'ششم'),
    (7, 'هفتم'),
    (8, 'هشتم'),
    (9, 'نهم'),
    (10, 'دهم'),
    (11, 'یازدهم'),
    (12, 'دوازدهم'),
)

GENDER = (
    ('MAN', 'مرد'),
    ('WOMAN', 'زن'),
)

CONTENT_TYPE = (
    (1, 'متن'),
    (2, 'فیلم'),
    (3, 'عکس'),
    (4, 'بازی'),
    (5, 'پاسخ'),
)

STUDENT_EXAM_STATUS = (
    (0, 'مجاز به ثبت‌نام'),
    (1, 'ثبت‌نام شده'),
    (2, 'پذیرفته‌شده'),
    (3, 'پذیرفته‌نشده'),
)

SESSION_TIME = 144000

# formula0
PROBLEM_SUBJECTS = (
    (0, 'اقتصاد - سطح ۱'),
    (1, 'اقتصاد - سطح ۲'),
    (2, 'ریاضی - سطح ۱'),
    (3, 'ریاضی - سطح ۲'),
    (4, 'زیست - سطح ۱'),
    (5, 'زیست - سطح ۲'),
    (6, 'شیمی - سطح ۱'),
    (7, 'شیمی - سطح ۲'),
    (8, 'فیزیک - سطح ۱'),
    (9, 'فیزیک - سطح ۲'),
    (10, 'کامپیوتر - سطح ۱'),
    (11, 'کامپیوتر - سطح ۲'),
    (12, 'نجوم - سطح ۱'),
    (13, 'نجوم - سطح ۲'),
)

PROBLEM_STATUS = (
    (0, 'گرفته نشده'),
    (1, 'گرفته شده'),
    (2, 'در حال تصحیح'),
    (3, 'صحیح شده'),
    (4, 'به مزایده گذاشته شده'),
    (5, 'در مزایده واگذار شده'),
)

GAME_MODE = (
    (0, 'عادی'),
    (1, 'مزایده'),
)

NEW_RESPONSE_TEMPLATE = '{{ "message": "{}", "data": {} }}'
