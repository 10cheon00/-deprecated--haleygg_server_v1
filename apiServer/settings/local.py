from apiServer.settings.base import *


INTERNAL_IPS = [
    '127.0.0.1'
]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

INSTALLED_APPS += [
    'corsheaders',
    'debug_toolbar',
    'rest_framework',
    'haleyGGapi',
]

# Cors Settings
CORS_ORIGIN_WHITELIST = [
    'http://127.0.0.1:8080',
    'http://localhost:8080'
]

CORS_ALLOW_CREDENTIALS = True

#Rest framework settings
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 2
}
