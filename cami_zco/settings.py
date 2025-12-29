"""
Django settings for cami.zco project.
"""

import os
from pathlib import Path
from decouple import config, Csv
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')  # Sin default: debe estar en .env

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

# Normalizar ALLOWED_HOSTS: remover protocolos, espacios y normalizar
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
    # Third party
    'cloudinary',
    'cloudinary_storage',
    # Local apps
    'catalogo',
    'pedidos',
    'contacto',
    'accounts',
    'dashboard',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Servir static files en producción
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
            ],
        },
    },
]

WSGI_APPLICATION = 'cami_zco.wsgi.application'


# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

DATABASE_URL = config('DATABASE_URL', default='sqlite:///db.sqlite3')

# En producción, SQLite no está permitido
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
    # Validar que DATABASE_URL esté bien formada
    try:
        DATABASES = {
            'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600)
        }
    except Exception as e:
        raise ValueError(
            f"Error al parsear DATABASE_URL: {e}. "
            "Verifique que DATABASE_URL tenga el formato correcto (postgresql://user:pass@host:port/db)"
        )


# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'es-ar'

TIME_ZONE = 'America/Argentina/Buenos_Aires'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# WhiteNoise configuration for serving static files in production
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Cloudinary settings
CLOUDINARY_CLOUD_NAME = config('CLOUDINARY_CLOUD_NAME')  # Sin default: debe estar en .env
CLOUDINARY_API_KEY = config('CLOUDINARY_API_KEY')  # Sin default: debe estar en .env
CLOUDINARY_API_SECRET = config('CLOUDINARY_API_SECRET')  # Sin default: debe estar en .env

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': CLOUDINARY_CLOUD_NAME,
    'API_KEY': CLOUDINARY_API_KEY,
    'API_SECRET': CLOUDINARY_API_SECRET,
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/6.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Security settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Session security
SESSION_COOKIE_HTTPONLY = True  # Prevents JavaScript access to session cookie
SESSION_COOKIE_SAMESITE = 'Lax'  # CSRF protection for cross-site requests
SESSION_COOKIE_AGE = 1209600  # 2 weeks (default Django)

# CSRF security
CSRF_COOKIE_HTTPONLY = False  # Must be False for AJAX requests, but we use SameSite
CSRF_COOKIE_SAMESITE = 'Lax'  # CSRF protection
# Normalizar CSRF_TRUSTED_ORIGINS: asegurar https:// y parsear correctamente
_csrf_origins_raw = config('CSRF_TRUSTED_ORIGINS', default='', cast=Csv())
CSRF_TRUSTED_ORIGINS = []
for origin in _csrf_origins_raw:
    origin = origin.strip()
    if origin:
        # Asegurar que tenga https://
        if not origin.startswith('https://') and not origin.startswith('http://'):
            origin = f'https://{origin}'
        # Remover trailing slash
        origin = origin.rstrip('/')
        CSRF_TRUSTED_ORIGINS.append(origin)

# Referrer policy
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'  # Limit referrer information leakage

if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True  # Only send over HTTPS
    CSRF_COOKIE_SECURE = True  # Only send over HTTPS
    # HSTS: Force HTTPS for 1 year (31536000 seconds)
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# WhatsApp number
WHATSAPP_NUMBER = config('WHATSAPP_NUMBER', default='5491112345678')

# Google Analytics 4
GA4_MEASUREMENT_ID = config('GA4_MEASUREMENT_ID', default='')

# Authentication
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/'

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
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
            'level': 'INFO',
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
            'level': config('DJANGO_LOG_LEVEL', default='INFO'),
            'propagate': False,
        },
    },
}

# Create logs directory if it doesn't exist
# En Vercel/serverless puede no tener permisos de escritura
try:
    os.makedirs(BASE_DIR / 'logs', exist_ok=True)
except (OSError, PermissionError):
    # En producción (Vercel) puede no tener permisos, usar solo console handler
    # Ajustar configuración de logging para serverless
    if 'file' in LOGGING.get('handlers', {}):
        LOGGING['handlers'] = {k: v for k, v in LOGGING['handlers'].items() if k == 'console'}
    if 'root' in LOGGING:
        LOGGING['root']['handlers'] = ['console']
    # También ajustar loggers individuales
    for logger_name, logger_config in LOGGING.get('loggers', {}).items():
        if 'handlers' in logger_config and 'file' in logger_config['handlers']:
            logger_config['handlers'] = [h for h in logger_config['handlers'] if h != 'file']
            if not logger_config['handlers']:
                logger_config['handlers'] = ['console']

# Validación de variables críticas: fallar explícitamente si faltan
if not SECRET_KEY:
    raise ValueError("SECRET_KEY no configurada. Debe estar definida en .env")

if not CLOUDINARY_CLOUD_NAME or not CLOUDINARY_API_KEY or not CLOUDINARY_API_SECRET:
    raise ValueError(
        "Variables de Cloudinary no configuradas. "
        "CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY y CLOUDINARY_API_SECRET deben estar en .env"
    )

# Validación adicional de DATABASE_URL en producción
if not DEBUG:
    if not DATABASE_URL or DATABASE_URL.startswith('sqlite'):
        raise ValueError(
            "DATABASE_URL debe estar configurada con PostgreSQL en producción. "
            "SQLite no está permitido."
        )

# Validaciones mejoradas para producción (Vercel)
# Usar warnings en lugar de ValueError para no romper el arranque
if not DEBUG:
    # Validar ALLOWED_HOSTS en producción
    if not ALLOWED_HOSTS or all(host in ['localhost', '127.0.0.1'] for host in ALLOWED_HOSTS):
        import warnings
        warnings.warn(
            "ALLOWED_HOSTS no está configurado para producción. "
            "Debe incluir dominios de Vercel (ej: *.vercel.app)",
            UserWarning
        )
    
    # Validar CSRF_TRUSTED_ORIGINS en producción
    if not CSRF_TRUSTED_ORIGINS:
        import warnings
        warnings.warn(
            "CSRF_TRUSTED_ORIGINS no está configurado en producción. "
            "Esto puede causar errores CSRF. Configurar con https://*.vercel.app",
            UserWarning
        )
