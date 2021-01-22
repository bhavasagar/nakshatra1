from django.urls import path
from . import views
from django.conf.urls import (handler400, handler403, handler404)
from allauth.account.views import SignupView
from .views import (    
    privacy,    
    Profile,    
    contact,
    # faqs,
    NumberSection,
    index,
    callback,
    payment,    
    rules,
    paid,
    home,
    payment_success,
    payment_failure,
)

app_name = 'core'

urlpatterns = [
    path('play/', NumberSection.as_view(), name='play'),    
    path(r'signup/<slug>', SignupView.as_view(), name="signup" ),    
    path('callback/', callback, name='callback'),
    path('payment_success/', payment_success, name='payment_success'),
    path('payment_failure/', payment_failure, name='payment_failure'),
    path('payment/', payment, name='payment'),
    path('', index, name='index'),
    path('rules/', rules, name='rules'),
    path('privacy/', privacy, name='privacy'),
    #path('sitemap.xml/', sitemap, name='sitemap.xml'),
    # path('robots.txt/', robots, name='robots.txt'),
    path('xyz/', home, name='home'),
    # path('refund/<slug>/', refund, name='refund'),
    path('profile/', Profile.as_view(), name='Profile'),   
    path('contact/', contact, name='contact'),
    path('paid/', paid, name='paid'),
]