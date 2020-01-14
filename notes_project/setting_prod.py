import os

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Email Reset Settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.live.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ.get('STICKYNOTESAPP_EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('STICKYNOTESAPP_EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
