from pathlib import Path
import os
from datetime import timedelta
from decouple import config
import dj_database_url


BASE_DIR = Path(__file__).resolve().parent.parent

# ========================
# SECURITY
# ========================

SECRET_KEY = config("SECRET_KEY")

DEBUG = config("DEBUG", default=False, cast=bool)



ALLOWED_HOSTS =['*']

# ========================
# INSTALLED APPS
# ========================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # THIRD PARTY
    'cloudinary',
    'cloudinary_storage',
    'axes',

    # YOUR APP
    'shop',
]

SITE_ID = 1

# ========================
# MIDDLEWARE
# ========================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'axes.middleware.AxesMiddleware',

    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
]

ROOT_URLCONF = 'snackshop.urls'

# ========================
# TEMPLATES
# ========================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'snackshop.wsgi.application'

# ========================
# DATABASE
# ========================

DATABASES = {
    'default': dj_database_url.config(
        default=config("DATABASE_URL"),
        conn_max_age=600,
        ssl_require=False
    )
}
# ========================
# PASSWORD VALIDATION
# ========================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ========================
# INTERNATIONALIZATION
# ========================

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ========================
# STATIC FILES
# ========================

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
WHITENOISE_USE_FINDERS = True

# ========================
# MEDIA FILES
# ========================

# MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ========================
# CLOUDINARY
# ========================

CLOUDINARY_STORAGE = {
    'cloud_name': config('CLOUDINARY_CLOUD_NAME'),
    'api_key': config('CLOUDINARY_API_KEY'),
    'api_secret': config('CLOUDINARY_API_SECRET'),
}

STORAGE ={
    'default':{
        'BACKEND': 'cloudinary_storage.storage.MediaCloudinaryStorage',
    },
    'staticfiles':{
        'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
    }
}
# ========================
# LOGIN / LOGOUT
# ========================

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/login/'

# ========================
# ACCOUNT SETTINGS
# ========================

ACCOUNT_LOGIN_METHODS = {'email', 'username'}

ACCOUNT_SIGNUP_FIELDS = [
    'email*',
    'username*',
    'password1*',
    'password2*'
]

ACCOUNT_EMAIL_VERIFICATION = 'none'
SOCIALACCOUNT_LOGIN_ON_GET = True

# ========================
# DJANGO AXES
# ========================

AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesStandaloneBackend',
    'django.contrib.auth.backends.ModelBackend',
]

AXES_ENABLED = False
AXES_FAILURE_LIMIT = 10
AXES_COOLOFF_TIME = 1
AXES_LOCKOUT_CALLABLE = None
# ========================
# DEFAULT PRIMARY KEY
# ========================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
SESSION_ENGINE = "django.contrib.sessions.backends.db"
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = "Lax"

CSRF_TRUSTED_ORIGINS = [
    "https://snackshoponline.onrender.com"
]