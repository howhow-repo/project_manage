# -*- encoding: utf-8 -*-
import environ
import os
from decouple import config

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, True)
)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CORE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='S#perS3crEt_007')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

# Assets Management
ASSETS_ROOT = os.getenv('ASSETS_ROOT', '/static/assets')

# path for documents & media
DOCS_ROOT = 'Docs'

# load production server from .env
ALLOWED_HOSTS        = ['localhost', 'localhost:85', '127.0.0.1',               config('SERVER', default='127.0.0.1')]

CSRF_TRUSTED_ORIGINS = ['http://localhost:85', 'http://127.0.0.1', 'https://' + config('SERVER', default='127.0.0.1')]


DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'letsencrypt',
    # 'apps.demo',                                    # Enable the inner demo (demo)
    'apps.authentication',
    'jsignature',
    # 'allauth',                                      # OAuth new
    # 'allauth.account',                              # OAuth new
    # 'allauth.socialaccount',                        # OAuth new
    # 'allauth.socialaccount.providers.github',       # OAuth new
    # 'allauth.socialaccount.providers.twitter',      # OAuth new
    'index',
    'employee',
    'doc_handle',
    'api',
    'material',
    'customer',
    'project',
    'notify',
    'quotation',
    'option_settings',
    'sslserver',
    'drf_yasg',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"
TEMPLATE_DIR = os.path.join(CORE_DIR, "apps/templates")  # ROOT dir for templates

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.context_processors.cfg_assets_root',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

if os.environ.get('DB_ENGINE') and os.environ.get('DB_ENGINE') == "mysql":
    DATABASES = {
      'default': {
        'ENGINE'  : 'django.db.backends.mysql',
        'NAME'    : config('DB_NAME', cast=str),
        'USER'    : config('DB_USERNAME', cast=str),
        'PASSWORD': config('DB_PASS', cast=str),
        'HOST'    : config('DB_HOST', cast=str),
        'PORT'    : config('DB_PORT', cast=int),
        },
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'db.sqlite3',
        }
    }

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

# AUTH_PASSWORD_VALIDATORS = [
#     {
#         'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
#     },
# ]

REST_FRAMEWORK = {
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser'
        )
}


AUTH_USER_MODEL = 'employee.User'

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'
USE_TZ = True
TIME_ZONE = 'Asia/Taipei'

USE_I18N = True

USE_L10N = True

USE_TZ = True

#############################################################

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'loggers': {
        'django': {
            'handler': ['console', 'file'],
            'level': config('DJANGO_LOG_LEVEL', default='INFO'),
            'propagate': False,
        },
        'django.server': {
            'handlers': ['console'],
            'level': config('DJANGO_LOG_LEVEL', default='INFO'),
            'propagate': False,
        },
        'apps': {
            'handlers': ['console', 'file'],
            'level': config('DJANGO_LOG_LEVEL', default='INFO'),
            'propagate': False,
        },
        'api': {
            'handlers': ['console', 'file'],
            'level': config('DJANGO_LOG_LEVEL', default='INFO'),
            'propagate': False,
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': './logs/log.log',
            'formatter': 'simple',
            'backupCount': 1,  # keep at most 10 log files
            'maxBytes': 5242880,  # 5*1024*1024 bytes (5MB)
        },
        'user_action': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': './logs/user_action.log',
            'formatter': 'simple',
            'backupCount': 1,  # keep at most 10 log files
            'maxBytes': 5242880,  # 5*1024*1024 bytes (5MB)
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'formatters': {
        'simple': {
            'format': '[%(levelname)s]%(name)s |  %(asctime)s |  %(message)s',
        },
    },
}

#############################################################
# SRC: https://devcenter.heroku.com/articles/django-assets

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_ROOT = os.path.join(CORE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(CORE_DIR, 'apps/static'),
)

#############################################################

SITE_ID                    = 1
ACCOUNT_EMAIL_VERIFICATION = 'none'

SOCIALACCOUNT_PROVIDERS = {}
