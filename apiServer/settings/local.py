from apiServer.settings.base import *


INTERNAL_IPS = [
    '127.0.0.1'
]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

INSTALLED_APPS += [
    'debug_toolbar',
    'rest_framework',
    'haleyGGapi',
]