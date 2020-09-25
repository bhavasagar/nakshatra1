from .base import *
import os

DEBUG = False
ALLOWED_HOSTS = ['nakshatra.fun','*']


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


PAYTM_MERCHANT_ID = '***'
PAYTM_SECRET_KEY = '***'
PAYTM_WEBSITE = 'DEFAULT'
PAYTM_CHANNEL_ID = 'WEB'
PAYTM_INDUSTRY_TYPE_ID = 'Retail'
