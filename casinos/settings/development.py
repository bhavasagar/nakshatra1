from .base import *
import os

DEBUG = True
ALLOWED_HOSTS = ['*']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'myprojectnakshatra',
        'USER': 'myprojectnakshatrauser',
        'PASSWORD': 'mypassword123nakshatra',
        'HOST': 'localhost',
        'PORT': '',
    }
}


PAYTM_MERCHANT_ID = 'UKwuJe94138276969334'
PAYTM_SECRET_KEY = 'gQ1L@5IwMhONe%3r'
PAYTM_WEBSITE = 'DEFAULT'
PAYTM_CHANNEL_ID = 'WEB'
PAYTM_INDUSTRY_TYPE_ID = 'Retail'