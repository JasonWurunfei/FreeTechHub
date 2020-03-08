"""
Django settings for FTH project.

Generated by 'django-admin startproject' using Django 3.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '6lz7v*ya4kvgd33jyei@9w_!zzp0sd-%6c+ree0d#ks=_y7+a4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.github',

    # third part packages
    'crispy_forms',
    'haystack',
    'whoosh',
    'jieba',
    'markdownx',
    'six',

    # system apps
    'blog.apps.BlogConfig',
    'comment.apps.CommentConfig',
    'likes.apps.LikesConfig',
    'home.apps.HomeConfig',
    'django.forms',
]
SITE_ID = 1
# add search engine (whoosh)
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'blog.whoosh_cn_backends.WhooshEngine',
        'PATH': os.path.join(BASE_DIR, 'whoosh_index'),
    }
}
HAYSTACK_SEARCH_RESULTS_PER_PAGE = 5      # 分页显示的数据量
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor' # 数据库改变自动更新索引


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'FTH.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR + "/templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                 # allauth 启动必须项
                'django.template.context_processors.request',

            ],
        },
    },
]

WSGI_APPLICATION = 'FTH.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

LOGIN_URL = ''
LOGIN_REDIRECT_URL = ''
LOGOUT_REDIRECT_URL = ''
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_REQUIRED = True
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS =3
ACCOUNT_LOGIN_ATTEMPTS_LIMIT =5
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION =False
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE =True
ACCOUNT_UNIQUE_EMAIL =True
ACCOUNT_USERNAME_MIN_LENGTH =5
SOCIALACCOUNT_AUTO_SIGNUP =False
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION =False
ACCOUNT_EMAIL_VERIFICATION ="mandatory"
LOGIN_REDIRECT_URL = '/blog/show/'
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL ='/accounts/login/'
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL ='/accounts/login/'
#use email to register
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = False # 是否使用TLS安全传输协议(用于在两个通信应用程序之间提供保密性和数据完整性。)
EMAIL_USE_SSL = True 
EMAIL_HOST = 'smtp.163.com' 
EMAIL_PORT = 465   
EMAIL_HOST_USER = ''       # 我自己的邮箱
EMAIL_HOST_PASSWORD = ''       # 我的邮箱授权码
EMAIL_SUBJECT_PREFIX = '[FREETECHHUB]'     # 为邮件Subject-line前缀,默认是'[django]'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER  # 与 EMAIL_HOST_USER 相同
PASSWORD_RESET_TIMEOUT_DAYS = 1

