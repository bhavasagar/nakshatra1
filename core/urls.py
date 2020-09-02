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
    #starter,
)

app_name = 'core'

urlpatterns = [
    path('play/', NumberSection.as_view(), name='play'),
    #path('starter/', starter, name='starter'),
    path(r'signup/<slug>', SignupView.as_view(), name="signup" ),    
    path('callback/', callback, name='callback'),
    path('payment/', payment, name='payment'),
    path('', index, name='index'),
    # path('simp/', simp, name='simp'),
    path('privacy/', privacy, name='privacy'),
    # path('sitemap.xml/', sitemap, name='sitemap.xml'),
    # path('robots.txt/', robots, name='robots.txt'),
    # path('myorders/', Myorders.as_view(), name='myorders'),
    # path('refund/<slug>/', refund, name='refund'),
    path('profile/', Profile.as_view(), name='Profile'),   
    path('contact/', contact, name='contact'),
    # path('faqs/', faqs, name='faqs'),
]