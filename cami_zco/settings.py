"""
Django settings for cami.zco project.
"""

import os
from pathlib import Path
from decouple import config, Csv
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = config('SECRET_KEY')

DEBUG = config('DEBUG', default='False').lower() in ('true', '1', 'yes')
_allowed_hosts_raw = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=Csv())
ALLOWED_HOSTS = [
    host.strip().replace('https://', '').replace('http://', '').split('/')[0]
    for host in _allowed_hosts_raw
    if host.strip()
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Local apps
    'catalogo',
    'pedidos',
    'contacto',
    'accounts',
    'dashboard',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'cami_zco.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'cami_zco.context_processors.whatsapp_number',
                'cami_zco.context_processors.google_analytics',
                'cami_zco.context_processors.configuracion_sitio',
            ],
        },
    },
]

WSGI_APPLICATION = 'cami_zco.wsgi.application'


DATABASE_URL = config('DATABASE_URL', default='sqlite:///db.sqlite3')

if not DEBUG and DATABASE_URL.startswith('sqlite'):
    raise ValueError(
        "SQLite no está permitido en producción. "
        "Debe configurar DATABASE_URL con PostgreSQL (ej: postgresql://user:pass@host/db)"
    )

if DATABASE_URL.startswith('sqlite'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    try:
    DATABASES = {
            'default': dj_database_url.parse(DATABASE_URL, conn_max_age=0)
    }
    except Exception as e:
        raise ValueError(
            f"Error al parsear DATABASE_URL: {e}. "
            "Verifique que DATABASE_URL tenga el formato correcto (postgresql://user:pass@host:port/db)"
        )



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



LANGUAGE_CODE = 'es-ar'

TIME_ZONE = 'America/Argentina/Buenos_Aires'

USE_I18N = True

USE_TZ = True



STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_ROOT.mkdir(exist_ok=True)
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_AGE = 1209600

CSRF_COOKIE_HTTPONLY = False
CSRF_COOKIE_SAMESITE = 'Lax'
_csrf_origins_raw = config('CSRF_TRUSTED_ORIGINS', default='', cast=Csv())
CSRF_TRUSTED_ORIGINS = []
for origin in _csrf_origins_raw:
    origin = origin.strip()
    if origin:
        if not origin.startswith('https://') and not origin.startswith('http://'):
            origin = f'https://{origin}'
        origin = origin.rstrip('/')
        CSRF_TRUSTED_ORIGINS.append(origin)

SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'

# Production security settings
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

WHATSAPP_NUMBER = config('WHATSAPP_NUMBER', default='5491112345678')
GA4_MEASUREMENT_ID = config('GA4_MEASUREMENT_ID', default='')

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'production': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO' if DEBUG else 'WARNING',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'WARNING',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': config('DJANGO_LOG_LEVEL', default='INFO' if DEBUG else 'WARNING'),
            'propagate': False,
        },
        'django.request': {
            'handlers': ['console', 'file'],
            'level': 'ERROR' if not DEBUG else 'INFO',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['console', 'file'],
            'level': 'WARNING',
            'propagate': False,
        },
    },
}

try:
os.makedirs(BASE_DIR / 'logs', exist_ok=True)
except (OSError, PermissionError):
    if 'file' in LOGGING.get('handlers', {}):
        LOGGING['handlers'] = {k: v for k, v in LOGGING['handlers'].items() if k == 'console'}
    if 'root' in LOGGING:
        LOGGING['root']['handlers'] = ['console']
    for logger_name, logger_config in LOGGING.get('loggers', {}).items():
        if 'handlers' in logger_config and 'file' in logger_config['handlers']:
            logger_config['handlers'] = [h for h in logger_config['handlers'] if h != 'file']
            if not logger_config['handlers']:
                logger_config['handlers'] = ['console']

if not SECRET_KEY:
    raise ValueError("SECRET_KEY no configurada. Debe estar definida en .env")

if not DEBUG:
    if not DATABASE_URL or DATABASE_URL.startswith('sqlite'):
        raise ValueError(
            "DATABASE_URL debe estar configurada con PostgreSQL en producción. "
            "SQLite no está permitido."
        )
    
    if not ALLOWED_HOSTS or all(host in ['localhost', '127.0.0.1'] for host in ALLOWED_HOSTS):
        import warnings
        warnings.warn(
            "ALLOWED_HOSTS no está configurado para producción. "
            "Debe incluir los dominios donde se accederá al sitio",
            UserWarning
        )
    
    if not CSRF_TRUSTED_ORIGINS:
        import warnings
        warnings.warn(
            "CSRF_TRUSTED_ORIGINS no está configurado en producción. "
            "Esto puede causar errores CSRF. Configurar con los orígenes permitidos",
            UserWarning
        )
