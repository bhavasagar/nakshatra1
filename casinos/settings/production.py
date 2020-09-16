from .base import *
# from decouple import config

DEBUG = config('DEBUG', cast=bool)
ALLOWED_HOSTS = ['nakshatra.fun','176.9.233.36']

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'}
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'naks',
        'USER': 'naks',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '',
    }
}

PAYTM_MERCHANT_ID = 'UKwuJe94138276969334'
PAYTM_SECRET_KEY = 'gQ1L@5IwMhONe%3r'
PAYTM_WEBSITE = 'DEFAULT'
PAYTM_CHANNEL_ID = 'WEB'
PAYTM_INDUSTRY_TYPE_ID = 'Retail'

SESSION_COOKIE_AGE = 60 * 60 * 24 * 30