import os
from .settings import BASE_DIR

ALLOWED_HOSTS = ['stickynotesapp.herokuapp.com']

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

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'staticbuild'),
]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
