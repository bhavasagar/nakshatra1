from .base import *
import os

DEBUG = True
ALLOWED_HOSTS = ['nakshatra.fun','*']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'myproject',
        'USER': 'myprojectuser',
        'PASSWORD': 'passwordnak',
        'HOST': 'localhost',
        'PORT': '',
    }
}

PAYTM_MERCHANT_ID = 'Paytm merchant id'
PAYTM_SECRET_KEY = 'Paytm key'
PAYTM_WEBSITE = 'DEFAULT' 
PAYTM_CHANNEL_ID = 'WEB'
PAYTM_INDUSTRY_TYPE_ID = 'Retail'
 
PAYMENT_URL_TEST = 'https://test.payu.in/_payment'
PAYMENT_URL_LIVE = 'https://secure.payu.in/_payment'
SERVICE_PROVIDER = "payu_paisa"
SALT = 'sfQeXDR7pB'
KEY = 'uw811sBS'
