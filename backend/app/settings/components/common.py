import os
from pathlib import Path

# Poprawiona wersja BASE_DIR
BASE_DIR    = Path(__file__).resolve().parent.parent
PROJECT_DIR = BASE_DIR.parent
SECRET_KEY = "21370000000"
DEBUG = 1
ALLOWED_HOSTS = ['*']

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # Poprawiona ścieżka
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

STATIC_URL  = "/static/"
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'staticfiles'),  # Poprawiona ścieżka
# ]
STATIC_ROOT = PROJECT_DIR / "static"

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

WSGI_APPLICATION = 'app.wsgi.application'

LANGUAGE_CODE = 'pl'

TIME_ZONE = 'UTC'

DATE_FORMAT = 'Y-m-d'

USE_I18N = True

USE_L10N = False

USE_TZ = True

FRONTEND_URL = 'http://localhost:8080'

CORS_ALLOW_CREDENTIALS = True
CSRF_TRUSTED_ORIGINS = [
    'http://146.59.126.193',
    'http://146.59.126.193:8000',
    'http://127.0.0.1:8080',
    'http://localhost:8080',
    'http://146.59.126.193:8080',
    'http://voltra.vps-ee0c2b62.vps.ovh.net',
'http://172.17.0.6:8080',
    'http://172.17.0.6:8000',
'http://172.17.0.6:5000',

]

CORS_ALLOW_ALL_ORIGINS = True
# CORS_ALLOWED_ORIGINS = [
#     'http://146.59.126.193',
#     'http://146.59.126.193:8000',
#     'http://127.0.0.1:8080',
#     'http://localhost:8080',
#     'http://146.59.126.193:8080',
#     'http://voltra.vps-ee0c2b62.vps.ovh.net',
#     'http://172.17.0.6:8080',
#     'http://172.17.0.6:8000',
# 'http://172.17.0.6:5000'
# ]
CORS_ALLOW_METHODS = ["GET", "POST", "OPTIONS"]
CORS_ALLOW_CREDENTIALS = True
FRONTEND_DOMAIN = FRONTEND_URL