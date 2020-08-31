from allauth.account.forms import SignupForm 
from django import forms 
from .models import UserProfile


class CustomSignupForm(SignupForm): 	    
    first_name = forms.CharField(max_length=30, label='Phone Number',widget=forms.TextInput(attrs={'placeholder': '9876543210'})) 
    last_name = forms.CharField(max_length=30, label='Refer Code',required=False,widget=forms.TextInput(attrs={'placeholder': 'QWERTY'})) 



