import os

ALLOWED_HOSTS = ['stickynotesapp.herokuapp.com']

# Email Reset Settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.live.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ.get('STICKYNOTESAPP_EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('STICKYNOTESAPP_EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Administrators to email server error in production
ADMIN_NAME = os.environ.get('STICKYNOTESAPP_ADMIN_NAME')
ADMIN_EMAIL = os.environ.get('STICKYNOTESAPP_ADMIN_EMAIL')
ADMINS = [(ADMIN_NAME, ADMIN_EMAIL), ]

# Default Server email address for error reporting
SERVER_EMAIL = os.environ.get('STICKYNOTESAPP_SERVER_EMAIL')
