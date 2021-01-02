from .base import *
import os

DEBUG = True
ALLOWED_HOSTS = ['nakshatra.fun','*']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'nak',
        'USER': 'postgres',
        'PASSWORD': '123',
        'HOST': 'localhost',
        'PORT': '',
    }
}

PAYTM_MERCHANT_ID = 'Paytm merchant id'
PAYTM_SECRET_KEY = 'Paytm key'
PAYTM_WEBSITE = 'DEFAULT'
PAYTM_CHANNEL_ID = 'WEB'
PAYTM_INDUSTRY_TYPE_ID = 'Retail'
