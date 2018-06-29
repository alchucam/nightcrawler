import os
import django_heroku
import dj_database_url
from unipath import Path
from decouple import config


from celery.schedules import crontab

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PROJECT_DIR = Path(__file__).parent

SECRET_KEY = config('SECRET_KEY')

DEBUG = config('DEBUG',default=False,cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=lambda v: [s.strip() for s in v.split(',')])

INSTALLED_APPS = [
    'nightcrawler.apps.services',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_windows_tools',
    'celerybeat_status',
    'django_celery_results',
    'django_celery_beat',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'nightcrawler.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['nightcrawler/templates/'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries':{
                'menu_helper': 'nightcrawler.apps.services.templatetags.menu_helper',
            }
        },
    },
]

WSGI_APPLICATION = 'nightcrawler.wsgi.application'


DATABASES = { 'default': dj_database_url.config(conn_max_age=600, ssl_require=True)}




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


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'


#CSS
STATICFILES_DIRS = [
PROJECT_DIR.child('static')
]

STATIC_ROOT = PROJECT_DIR.parent.parent.child('static')


CELERY_BROKER_URL = config('CELERY_BROKER_URL')

CELERY_IMPORTS = ('nightcrawler.tasks',)

CELERYBEAT_SCHEDULER = "django_celery_beat.schedulers.DatabaseScheduler"

CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
BROKER_HEARTBEAT = 0
BROKER_HEARTBEAT_CHECKRATE = 0
CELERY_TIMEZONE = 'UTC'
CELERY_ENABLE_UTC = True

CELERYBEAT_SCHEDULE = {
    'keep_run': {
        'task':'nightcrawler.tasks.keep_it',
        'schedule': 60*120, #2 hour
    },
}

NYTIMES_API_KEY= config('NYTIMES_API_KEY')

django_heroku.settings(locals())

BROKER_POOL_LIMIT = 3
