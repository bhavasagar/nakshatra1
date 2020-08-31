from django.urls import path
from . import views
from django.conf.urls import (handler400, handler403, handler404)
from allauth.account.views import SignupView
from .views import (    
    callback,
    payment,
    # ordercallback,
    # landing,
    # simp,
    privacy,
    # returnpolicy,
    # about,
    # temp,
    # sitemap,
    # robots,
    # Myorders,
    # refund,
    Profile,
    # test,
    # categories,
    # push,
    # clubpayment,
    # refreshprod,
    contact,
    # faqs,
    NumberSection,
    index,
)

app_name = 'core'

urlpatterns = [
    path('play/', NumberSection.as_view(), name='play'),
    path(r'signup/<slug>', SignupView.as_view(), name="signup" ),    
    path('callback/', callback, name='callback'),
    path('payment/', payment, name='payment'),
    # path('ordercallback/', ordercallback, name='ordercallback'),
    # path('clubpayment/', clubpayment, name='clubpayment'),
    path('', index, name='index'),
    # path('simp/', simp, name='simp'),
    path('privacy/', privacy, name='privacy'),
    # path('returnpolicy/', returnpolicy, name='returnpolicy'),
    # path('about/', about, name='about'),
    # path('tests/', temp.as_view(), name='temp'),
    # path('sitemap.xml/', sitemap, name='sitemap.xml'),
    # path('robots.txt/', robots, name='robots.txt'),
    # path('myorders/', Myorders.as_view(), name='myorders'),
    # path('refund/<slug>/', refund, name='refund'),
    path('profile/', Profile.as_view(), name='Profile'),
    # path('refreshpaid/', test, name='test'),
    # path('refreshprod/', refreshprod, name='refreshprod'),
    # path('sw.js/', push, name='push'),
    # path('categories/<slug>/', categories, name='categories'),
    path('contact/', contact, name='contact'),
    # path('faqs/', faqs, name='faqs'),
]