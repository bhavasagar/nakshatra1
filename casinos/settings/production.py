from .base import *
# from decouple import config

DEBUG = config('DEBUG', cast=bool)
ALLOWED_HOSTS = ['nakshatra.fun','**']

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'}
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '**',
        'USER': '**',
        'PASSWORD': '**',
        'HOST': 'localhost',
        'PORT': '',
    }
}

PAYTM_MERCHANT_ID = '**'
PAYTM_SECRET_KEY = '**'
PAYTM_WEBSITE = 'DEFAULT'
PAYTM_CHANNEL_ID = 'WEB'
PAYTM_INDUSTRY_TYPE_ID = 'Retail'

SESSION_COOKIE_AGE = 60 * 60 * 24 * 30
