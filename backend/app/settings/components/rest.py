import os
from datetime import timedelta
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (#
        'rest_framework.permissions.IsAuthenticated', #
    ),#
    'DEFAULT_PAGINATION_CLASS': 'apps.common.utils.paginator.CurrentPagePagination',
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': os.getenv('THROTTLE_RATE_ANON'),
    },
    'PAGE_SIZE': 100,
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=20),  # Jak długo ważny jest access token#TODO
    'REFRESH_TOKEN_LIFETIME': timedelta(days=20),  # Jak długo ważny jest refresh token
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',  # Domyślny algorytm JWT
    'SIGNING_KEY': "g7zOdg&YKVLMsEA5ZOJY72yctt4h9^2s",  # Musi być ten sam co w Django
    'AUTH_HEADER_TYPES': ('Bearer',),
}