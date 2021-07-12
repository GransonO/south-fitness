"""
Django settings for south_fitness_server project.

Generated by 'django-admin startproject' using Django 2.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import environ

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'j43uwc5v2q^(p%s8xco0+$tmzx)$2h_7*+o)hg6ws4*2l*6x6c'
REFRESH_TOKEN_SECRET = 'j436uwc5v2q^(p%s8xco0+$tzx)$2h_7*+o)hg6wvs4*2l*6x6c'
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# DEBUG = False

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

environ.Env.read_env(env_file=os.path.join(BASE_DIR, '.env'))

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # created apps
    'south_fitness_server.apps.notifications',
    'south_fitness_server.apps.support',
    'south_fitness_server.apps.videos',
    'south_fitness_server.apps.profiles',
    'south_fitness_server.apps.fcm',
    'south_fitness_server.apps.staff',
    'south_fitness_server.apps.blogs',
    'south_fitness_server.apps.authentication',
    'south_fitness_server.apps.teams',
    'south_fitness_server.apps.challenges',
    'south_fitness_server.apps.chats',

    # third party apps
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'background_task',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'south_fitness_server.apps.authentication.CustomAuth.SafeJWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # third party apps
    'corsheaders.middleware.CorsMiddleware',
    'bugsnag.django.middleware.BugsnagMiddleware',

    # recomended for serving static files
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'south_fitness_server.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'south_fitness_server.wsgi.application'
CORS_ORIGIN_ALLOW_ALL = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "south-fitness.herokuapp.com", 'southfitness.epitomesoftware.live']
AUTH_USER_MODEL = 'authentication.User'
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.Argon2PasswordHasher',
]
AUTHENTICATION_BACKENDS = (
        'django.contrib.auth.backends.ModelBackend',
    )
# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': env.db()
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

# Configure service for static files within the django app
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

BUGSNAG = {
    'api_key': '40400b3f45e41e2003dc1466dd81d8a8',
    'project_root': PROJECT_ROOT
}

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)

# Efficiently resizes the served static files.
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Email data
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = ''
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
DEFAULT_FROM_EMAIL = 'Southfitness'
