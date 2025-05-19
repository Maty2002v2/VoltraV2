INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',

    'rest_framework',
    'drf_spectacular',
    'django_filters',
    'corsheaders',
    'django_celery_beat',

    'app',
    'apps.common',
    'apps.division',
    'apps.files',
    'apps.users',
    'apps.points',
]
