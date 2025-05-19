import os

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

# PASSWORD_LIFESPAN_DAYS = int(os.getenv('PASSWORD_LIFESPAN_DAYS'))
# INVALID_LOGIN_ATTEMPTS = int(os.getenv('INVALID_LOGIN_ATTEMPTS'))
PASSWORD_LIFESPAN_DAYS = 30000
INVALID_LOGIN_ATTEMPTS = 30000