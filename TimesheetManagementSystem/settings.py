"""
Django settings for TimesheetManagementSystem project.

Generated by 'django-admin startproject' using Django 2.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '33o3)02k$7)x6qja60p6uwnrqx2o$h@ya5o39id39m@r_rsxw('

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_filters',
    'rest_framework',
    'rest_framework_swagger',
    'tracker',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'TimesheetManagementSystem.urls'

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

WSGI_APPLICATION = 'TimesheetManagementSystem.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'TMS',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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

LOGIN_URL = 'login/'

LOGIN_REDIRECT_URL = 'login/'

LOGOUT_URL = 'logout/'

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'


# MEDIA files
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


# Required choices variables
GENDER_CHOICES = (('M', 'Male'), ('F', 'Female'))
STATUS_CHOICES = (('Active', 'Active'), ('Inactive', 'Inactive'), ('Delete', 'Delete'))
PROJECT_STATUS = (('In progress', 'In progress'), ('Complete', 'Complete'), ('On Hold', 'On Hold'), ('Delete', 'Delete'))
EMPLOYEE_STATUS = (('Available', 'Available'), ('Unavailable', 'Unavailable'), ('Vacation', 'On Vacation'),\
                   ('Delete', 'Delete'))
EMPLOYEMENT_TYPE = (('Full Time', 'Full Time'), ('Part Time', 'Part Time'))
PAY_RATE_TYPE = (('Hourly', 'Hourly'), ('Daily', 'Daily'), ('Weekly', 'Weekly'), ('Bi-Weekly', 'Bi-Weekly'),\
                 ('Monthly', 'Monthly'), ('Yearly', 'Yearly'))
TIMESHEET_STATUS = (('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected'), ('Delete', 'Delete'))
INVOICE_STATUS = (('Paid', 'Paid'), ('Unpaid', 'Unpaid'), ('Delete', 'Delete'))

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',)
}
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

# Logs configuration
LOG_ROOT = os.path.join(BASE_DIR, 'docs/logs/')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'null': {
            'class': 'logging.NullHandler',
        },
        'tracker_log_file': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'formatter': 'verbose',
            'class': 'logging.FileHandler',
            'filename': LOG_ROOT+'tracker.log',
        },
    },
    'loggers': {
        'tracker_log': {
            'handlers': ['tracker_log_file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'py.warnings': {
            'handlers': ['console'],
        },
    },
}
