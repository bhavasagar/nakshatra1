from django.db.models.signals import post_save
from django.conf import settings
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.db.models import Sum
from django.shortcuts import reverse
from django.utils import timezone

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    userphoto = models.ImageField(upload_to='images/', null=True,blank=True)
    phone_number = models.CharField(default=False, max_length=30)
    total_amount = models.FloatField(default="0", max_length=5)
    won = models.FloatField(default="0", max_length=5)    
    refer_income = models.FloatField(default="0", max_length=5)
    ref_code = models.CharField(default=False, max_length=15)
    refer = models.CharField(default=False, max_length=15)

    def __str__(self):
        return self.user.username 

    def get_absolute_url(self):
        return reverse("core:signup", kwargs={
            'slug': self.ref_code
        })    

class RedEnvelope(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.FloatField(default="0", max_length=5)

    def __str__(self):
        return self.user.username

class History(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    id_made = models.CharField(max_length=100,null=True,blank=True)
    investment = models.CharField(max_length=10,null=True,blank=True)
    color_selected = models.CharField(max_length=10,null=True,blank=True)
    num_selected = models.CharField(max_length=10,null=True,blank=True)
    paid = models.BooleanField(default=False)
    result = models.CharField(max_length=10,default="unknown",null=True,blank=True)
    mode = models.CharField(max_length=10,default="unknown",null=True,blank=True)
    def __str__(self):
        return self.user.username      

class GoldGame(models.Model):    
    mode = models.CharField(max_length=10,null=True, blank=True)
    total_investment = models.CharField(max_length=10,default='0',null=True,blank=True)    
    green_investment = models.FloatField(max_length=10,default='0',null=True, blank=True)    
    red_investment = models.FloatField(max_length=10,default='0',null=True, blank=True)
    purple_investment = models.FloatField(max_length=10,default='0',null=True, blank=True)    
    n_investment = ArrayField(models.CharField(max_length=10),size=10,null=True, blank=True,default=list)
    result = models.CharField(max_length=10,default="unknown",null=True, blank=True)
    color = models.CharField(max_length=10,default="unknown",null=True, blank=True)
    id_made = models.CharField(max_length=20,default="unknown",null=True, blank=True)
    def __str__(self):
        return self.mode 
        
class SilverGame(models.Model):    
    mode = models.CharField(max_length=10,null=True, blank=True)
    total_investment = models.CharField(max_length=10,default='0',null=True,blank=True)    
    green_investment = models.FloatField(max_length=10,default='0',null=True, blank=True)    
    red_investment = models.FloatField(max_length=10,default='0',null=True, blank=True)
    purple_investment = models.FloatField(max_length=10,default='0',null=True, blank=True)    
    n_investment = ArrayField(models.CharField(max_length=10),size=10,null=True, blank=True,default=list)
    result = models.CharField(max_length=10,default="unknown",null=True, blank=True)
    color = models.CharField(max_length=10,default="unknown",null=True, blank=True)
    id_made = models.CharField(max_length=20,default="unknown",null=True, blank=True)
    def __str__(self):
        return self.mode 

class DiamondGame(models.Model):    
    mode = models.CharField(max_length=10,null=True, blank=True)
    total_investment = models.CharField(max_length=10,default='0',null=True,blank=True)    
    green_investment = models.FloatField(max_length=10,default='0',null=True, blank=True)    
    red_investment = models.FloatField(max_length=10,default='0',null=True, blank=True)
    purple_investment = models.FloatField(max_length=10,default='0',null=True, blank=True)    
    n_investment = ArrayField(models.CharField(max_length=10),size=10,null=True, blank=True,default=list)
    result = models.CharField(max_length=10,default="unknown",null=True, blank=True)
    color = models.CharField(max_length=10,default="unknown",null=True, blank=True)
    id_made = models.CharField(max_length=20,default="unknown",null=True, blank=True)
    def __str__(self):
        return self.mode 

class OtherGame(models.Model):    
    mode = models.CharField(max_length=10,null=True, blank=True)
    total_investment = models.CharField(max_length=10,default='0',null=True,blank=True)    
    green_investment = models.FloatField(max_length=10,default='0',null=True, blank=True)    
    red_investment = models.FloatField(max_length=10,default='0',null=True, blank=True)
    purple_investment = models.FloatField(max_length=10,default='0',null=True, blank=True)    
    n_investment = ArrayField(models.CharField(max_length=10),size=10,null=True, blank=True,default=list)
    result = models.CharField(max_length=10,default="unknown",null=True, blank=True)
    color = models.CharField(max_length=10,default="unknown",null=True, blank=True)
    id_made = models.CharField(max_length=20,default="unknown",null=True, blank=True)
    def __str__(self):
        return self.mode                     

class Transaction(models.Model):
    made_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='transactions', 
                                on_delete=models.CASCADE)
    made_on = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    order_id = models.CharField(unique=True, max_length=100, null=True, blank=True)
    checksum = models.CharField(max_length=200, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.order_id is None and self.made_on and self.id:
            self.order_id = self.made_on.strftime('PAY2ME%Y%m%dODR') + str(self.id)
        return super().save(*args, **kwargs)

# class Item(models.Model):
#     title = models.CharField(max_length=100)
#     price = models.FloatField()
#     tag = models.CharField(max_length=10,blank=True,null=True,default='New')        
#     category = models.CharField(max_length=20)
#     label = models.CharField(max_length=10)
#     slug = models.SlugField()
#     description = models.TextField()
#     image = models.ImageField()        
#     def __str__(self):
#         return self.title
        
#     def get_absolute_url(self):
#         return reverse("core:product", kwargs={
#             'slug': self.slug
#         })


class Paytm_history(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='rel_payment_order_paytm', on_delete=models.CASCADE, null=True, default=None)
    MERC_UNQ_REF = models.IntegerField('USER ID')
    ORDERID = models.CharField('ORDER ID', max_length=30)
    TXNDATE = models.DateTimeField('TXN DATE', default=timezone.now)
    TXNID = models.CharField('TXN ID', max_length=100)
    BANKTXNID = models.CharField('BANK TXN ID', max_length=100, null=True, blank=True)
    BANKNAME = models.CharField('BANK NAME', max_length=50, null=True, blank=True)
    RESPCODE = models.IntegerField('RESP CODE')
    PAYMENTMODE = models.CharField('PAYMENT MODE', max_length=10, null=True, blank=True)
    CURRENCY = models.CharField('CURRENCY', max_length=4, null=True, blank=True)
    GATEWAYNAME = models.CharField("GATEWAY NAME", max_length=30, null=True, blank=True)
    MID = models.CharField(max_length=40)
    RESPMSG = models.TextField('RESP MSG', max_length=250)
    TXNAMOUNT = models.FloatField('TXN AMOUNT')
    STATUS = models.CharField('STATUS', max_length=12)

    def __str__(self):
        return '%s  (%s)' % (self.user.username ,self.pk)


    def __unicode__(self):
        return self.STATUS


    def __iter__(self):
        for field_name in [f.name for f in self._meta.get_fields()]:
            value = getattr(self, field_name, None)
            yield (field_name, value)
            

class withdraw_requests(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.CharField(default=False, max_length=15)
    UPIID = models.CharField(default=False, max_length=15)
    paid = models.BooleanField(default=False)  
    made_on = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return '%s  (%s)' % (self.amount ,self.UPIID)

class Carousal(models.Model):
    for_carousal = models.CharField(max_length=15)
    image = models.ImageField(upload_to='images/', null=True)
    heading = models.CharField(max_length=15)
    description = models.CharField(max_length=100)
    urlfield = models.URLField(max_length = 200)    

# class Carousal(models.Model):
#     carousal = models.many_to_one(Carousal, on_delete=models.CASCADE)    

# class Multi_Carousal(models.Model):
#     carousal = models.ForeignKey(Carousal, on_delete=models.CASCADE)    

# class Team(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='rel_team', on_delete=models.CASCADE)
#     name = models.CharField(max_length=20,default="HKR")
#     img = models.ImageField()
#     desig = models.CharField(max_length=20,default="CEO")
#     opinion = models.TextField()
#     team = models.CharField(default=False,null=True,blank=True,max_length=30)
#     facebook = models.URLField(max_length = 200)
#     twitter = models.URLField(max_length = 200)
#     email = models.EmailField()
    
#     def __str__(self):
#         return self.user.username
        
class Contact(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.CharField(max_length=500)
    
    def __str__(self):
        return self.name

# class FAQs(models.Model):
#     question = models.CharField(max_length=50)
#     answer = models.CharField(max_length=500)
    
#     def __str__(self):
#         return self.question
        
#     class Meta:
#         verbose_name_plural = 'FAQs'

import random as rd
def refgenrator():
    l=rd.choices(range(65,90),k=6)
    c=""
    for i in range(len(l)):
        c+=chr(l[i])
    return str(c) 

def userprofile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        userprofile = UserProfile.objects.create(user=instance) 
        userprofile.ref_code = refgenrator()
        userprofile.phone_number = instance.first_name        
        if instance.last_name:
            try:
                up = UserProfile.objects.get(ref_code=instance.last_name) 
                userprofile.refer = up.user.username
            except:
                pass
        instance.first_name = ""
        instance.last_name = ""
        instance.save()
        userprofile.save()

post_save.connect(userprofile_receiver, sender=settings.AUTH_USER_MODEL)