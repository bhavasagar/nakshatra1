from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.utils import timezone
from .models import History, UserProfile, Transaction, Paytm_history, GoldGame, SilverGame, DiamondGame, OtherGame, withdraw_requests, Contact, Carousal, RedEnvelope, Carousal1, Carousal2, Carousal3, Notifications, Home_description, Payu 
import random
from django.shortcuts import reverse
import string
import hashlib
import requests
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login as auth_login
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from .paytm import generate_checksum, verify_checksum
import smtplib
from django.core.paginator import Paginator
from email.message import EmailMessage
from datetime import datetime, timedelta
from django.db.models import Q
from django.db.models.functions import ( ExtractDay, ExtractHour, ExtractMinute, ExtractMonth, ExtractSecond, ExtractWeek, ExtractWeekDay, ExtractYear )
from django.utils.html import format_html
import pytz
from random import randint
from django.template.context_processors import csrf

utc=pytz.UTC     
            

def refgenrator(name):
    l=random.choices(string.ascii_lowercase+string.ascii_uppercase,k=6)
    c=""
    for i in range(len(l)):
        c+=chr(l[i])
    return str(c)

def privacy(request):
    return render(request,"privacy.html")

def rules(request):
    return render(request,"rules.html")            
    
# def sitemap(request):
#     return render(request, 'sitemap.xml')

# def robots(request):
#     return render(request, 'robots.txt')
    

def paid(request, slug):     
     server = smtplib.SMTP_SSL('smtp.gmail.com',465)
     server.login('nakshatra.fun@gmail.com','ganesh@123')
     objs = withdraw_requests.objects.filter(paid=True)
     for i in objs:
         try:           
             msg1 = EmailMessage()
             msg1.set_content("This is a computer generated email, don't reply to this mail.\n This mail is to inform you that your withdraw request is processed and amount Rs. "+  str(i.amount)+" \n Regards Nakshatra Team.")
             msg1['Subject'] = 'Withdraw Request - Nakshatra'
             msg1['From'] = "nakshatra.fun@gmail.com"
             msg1['To'] = i.user.email
             server.send_message(msg1)
         except:
             pass
     server.quit()
     return render(request,"paid.html")

class Profile(LoginRequiredMixin, View):
    template_name = "profile.html"
    def get(self, *args, **kwargs):
        context={}                
        recharges = Paytm_history.objects.filter(user=self.request.user,STATUS='TXN_SUCCESS').order_by('-id')
        context['recharges'] = recharges
        if recharges.count()>10:
            context['recharges'] = recharges[:10]
        withdrawls = withdraw_requests.objects.filter(user=self.request.user).order_by('-id')
        context['withdrawls'] = withdrawls
        if withdrawls.count()>10:
            context['withdrawls'] = withdrawls[:10]
        history = History.objects.filter(user=self.request.user).order_by('-id')
        context['history'] = history
        if history.count()>10:
            context['history'] = history[:10]
        refers = UserProfile.objects.filter(refer=self.request.user.username).order_by('-id')
        context['refers'] = refers       
        if refers.count()>10: 
            context['refers'] = refers[:10]
        re = RedEnvelope.objects.filter(user=self.request.user)
        context['rv'] = re  
        notes = Notifications.objects.all()
        context['notes'] = notes
        return render(self.request,self.template_name,context=context)
    def post(self, *args, **kwargs):
        if self.request.method == 'POST':            
            if self.request.FILES.get('image'):
                self.request.user.userprofile.userphoto = self.request.FILES.get('image')
                self.request.user.userprofile.save()
            if self.request.POST.get('pnumber'):
                if (len(self.request.POST.get('pnumber'))>9 and len(self.request.POST.get('pnumber'))<20): 
                    self.request.user.userprofile.phone_number = self.request.POST.get('pnumber')
            if self.request.POST.get('uname'):
                if len(self.request.POST.get('uname'))>0:
                    self.request.user.username = self.request.POST.get('uname')
                    self.request.user.save()
            if self.request.POST.get('email'):
                if len(self.request.user.email)>0:
                    self.request.user.email = self.request.POST.get('email')
                    self.request.user.save()
                    
            if self.request.POST.get('upiid'):    
                noreqs = withdraw_requests.objects.filter(Q(user=self.request.user)&Q(made_on__gte=datetime.now()-timedelta(hours=24)))
                if noreqs.count() > 0:
                    messages.success(self.request,'Only one request is allowed in a day.')       
                    context={}        
                    return redirect('core:Profile')
                if (len(self.request.POST.get('upiid'))>5 and len(self.request.POST.get('upiid'))<25) and int(self.request.POST.get('amt'))>=100 and float(self.request.user.userprofile.total_amount)>=int(self.request.POST.get('amt')): 
                    withdraw_request = withdraw_requests.objects.create(amount=str(self.request.POST.get('amt')),UPIID=self.request.POST.get('upiid'),user=self.request.user)         
                    self.request.user.userprofile.total_amount = float(self.request.user.userprofile.total_amount) - float(self.request.POST.get('amt'))
                    self.request.user.userprofile.save()
                    messages.success(self.request,'Money will be added to your account in 45 hours.')       
                if not (len(self.request.POST.get('upiid'))>5 and len(self.request.POST.get('upiid'))<25):                    
                    messages.warning(self.request,'Invalid details entered.')
                if not int(self.request.POST.get('amt'))>=100:
                    messages.warning(self.request,'Please enter amount greater than or equal to 100.')
                if not float(self.request.user.userprofile.total_amount)>=int(self.request.POST.get('amt')): 
                    messages.warning(self.request,'Insufficient balance in your wallet.')                    
            context={}        
            return redirect('core:Profile')

# def faqs(request):
#     faqs= FAQs.objects.all()
#     context={'faq':faqs}
#     return render(request, "faqs.html", context)
    
def contact(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")
        contactform = Contact.objects.create(name=name,email=email,subject=subject)
        contactform.subject = subject
        contactform.message = message
        contactform.save()  
        msg="Your complaint is submitted."
        return render(request, "contact.html", {'msg':msg})
    return render(request, "contact.html")

def error_404(request, exception):
        data = {}
        return render(request,'404error.html', data)

#def error_500(request,  exception):
 #       data = {}
  #      return render(request,'404error.html', data)
        
def error_413(request,  exception):
        data = {}
        return render(request,'404error.html', data)  
    

@login_required
def payment(request):
    if request.method == "GET":
        return render(request, 'payments.html')
    if request.method == "POST":
        try:
            amt = request.POST.get('amt')
            if not float(amt)>99:
                messages.info(request,'Amount should be greater than Rs.100')    
                return render(request, 'payments.html')
        except:
            messages.info(request,'Enter Valid amount')
            return render(request, 'payments.html')
        transaction = Transaction.objects.create(made_by=request.user, amount=amt)
        transaction.save()
        data = {}
        txnid = get_transaction_id()
        hash_ = generate_hash(request, txnid, amt)
        hash_string = get_hash_string(request, txnid, amt)
        payu =Payu.objects.create(trans_id=txnid,status="Intiated")
        data["action"] = settings.PAYMENT_URL_LIVE 
        data["amount"] = float(amt)
        data["productinfo"]  = 'Recharge'
        data["key"] = settings.KEY
        data["txnid"] = txnid
        data["hash"] = hash_
        data["hash_string"] = hash_string
        data["firstname"] = str(request.user.username)
        data["email"] = 'nak54321go@gmail.com'
        data["phone"] = '8978305022'
        data["service_provider"] = settings.SERVICE_PROVIDER
        data["furl"] = request.build_absolute_uri(reverse("core:payment_failure"))
        data["surl"] = request.build_absolute_uri(reverse("core:payment_success"))
        
        return render(request, "pay.html", data)        

def generate_hash(request, txnid, amt): 
    try:
        hash_string = get_hash_string(request,txnid,amt)
        generated_hash = hashlib.sha512(hash_string.encode('utf-8')).hexdigest().lower()
        return generated_hash
    except Exception as e:       
        logging.getLogger("error_logger").error(traceback.format_exc())
        return None

def get_hash_string(request, txnid, amt):
    hash_string = settings.KEY+"|"+txnid+"|"+str(float(amt))+"|"+'Recharge'+"|"
    hash_string += str(request.user.username)+"|"+'nak54321go@gmail.com'+"|"
    hash_string += "||||||||||"+settings.SALT

    return hash_string


def get_transaction_id():
    hash_object = hashlib.sha256(str(randint(0,9999)).encode("utf-8"))
    txnid = hash_object.hexdigest().lower()[0:32]
    return txnid

@csrf_protect
@csrf_exempt
def payment_success(request):
    c = {}
    c.update(csrf(request))
    status=request.POST["status"]
    firstname=request.POST["firstname"]
    amount=request.POST["amount"]
    txnid=request.POST["txnid"]
    posted_hash=request.POST["hash"]
    key=request.POST["key"]
    productinfo=request.POST["productinfo"]
    email=request.POST["email"]
    salt=settings.SALT
    try:
      additionalCharges=request.POST["additionalCharges"]
      retHashSeq=additionalCharges+'|'+salt+'|'+status+'|||||||||||'+email+'|'+firstname+'|'+productinfo+'|'+amount+'|'+txnid+'|'+key
    except Exception:
      retHashSeq = salt+'|'+status+'|||||||||||'+email+'|'+firstname+'|'+productinfo+'|'+amount+'|'+txnid+'|'+key
    hashh=hashlib.sha512(retHashSeq.encode("utf-8")).hexdigest().lower()
    if hashh !=posted_hash:
      message="Invalid Transaction. Please try again"
    else:
      message="Payment Failed | Please try again"
      cust = User.objects.get(username=firstname)
      up = UserProfile.objects.get(user=cust)    
      payu = Payu.objects.get(trans_id=txnid)
      if not payu.added:                                   
        up.total_amount = float(up.total_amount) + float(amount)
        up.save()
        payu.added = True        
        payu.save()
      payu.status = "success"
      payu.save()
      msg = "PS"
      oid =  str(txnid)
      ta =  str(amount)
    return render(request,'success.html',{"message":message+"Your account balance is "+str(up.total_amount)})
 
@csrf_protect
@csrf_exempt
def payment_failure(request):
    c = {}
    c.update(csrf(request))
    status=request.POST["status"]
    firstname=request.POST["firstname"]
    amount=request.POST["amount"]
    txnid=request.POST["txnid"]
    posted_hash=request.POST["hash"]
    key=request.POST["key"]
    productinfo=request.POST["productinfo"]
    email=request.POST["email"]
    salt=settings.SALT
    try:
      additionalCharges=request.POST["additionalCharges"]
      retHashSeq=additionalCharges+'|'+salt+'|'+status+'|||||||||||'+email+'|'+firstname+'|'+productinfo+'|'+amount+'|'+txnid+'|'+key
    except Exception:
      retHashSeq = salt+'|'+status+'|||||||||||'+email+'|'+firstname+'|'+productinfo+'|'+amount+'|'+txnid+'|'+key
    hashh=hashlib.sha512(retHashSeq.encode("utf-8")).hexdigest().lower()
    if hashh !=posted_hash:
      message="Invalid Transaction. Please try again"
    else:
      message="Payment Failed | Please try again"
      cust = User.objects.get(username=firstname)
      up = UserProfile.objects.get(user=cust)                                 
      payu = Payu.objects.get(trans_id=txnid)
      payu.status = "failure"
      payu.save()
      msg = "PF"
      oid =  str(txnid)
      ta =  str(amount)
    return render(request,'success.html',{"message":message+"Your account balance is "+str(up.total_amount)})

@csrf_exempt
def callback(request): 
    if request.method == "POST":
        user = request.user
        MERCHANT_KEY = settings.PAYTM_SECRET_KEY
        data_dict = {}
        data_dict = dict(request.POST.items())

        verify = verify_checksum(data_dict, MERCHANT_KEY, data_dict['CHECKSUMHASH'])            
        if verify:
            for key in request.POST:                                                                      
                if key == "BANKTXNID" or key == "RESPCODE":
                    if request.POST[key]:
                        data_dict[key] = int(request.POST[key])
                    else:
                        data_dict[key] = 0
                elif key == "TXNAMOUNT":
                    data_dict[key] = float(request.POST[key])
            Paytm_history.objects.create(user_id = data_dict['MERC_UNQ_REF'], **data_dict)
            cust = User.objects.get(id=data_dict['MERC_UNQ_REF'])
            up = UserProfile.objects.get(user=cust)                                 
            if data_dict['STATUS'] == 'TXN_SUCCESS':                                
                up.total_amount = float(up.total_amount) + float(data_dict['TXNAMOUNT'])
                up.save()
                msg = "PS"
            else:
                msg = "PF"
            oid =  str(data_dict['ORDERID'])
            ta =  str(data_dict['TXNAMOUNT'])
            return render(request, "callback.html", {"paytm":data_dict, 'user': user, 'msg':msg, 'oid':oid, 'ta':ta})
        else:
            return HttpResponse("checksum verify failed")
    return HttpResponse(status=200)

	
def signup(self, request, user):   	    				    
    user.first_name = self.cleaned_data['first_name']
    user.last_name = self.cleaned_data['last_name'] 
    user.save()     
    return user     

def index(request):
    context={}
    try:
        c = Carousal.objects.all()[0]
        carousals = Carousal.objects.all().exclude(id=c.id)
        context['carousals'] = carousals
        context['c'] = c
        c1 = Carousal1.objects.all()[0]
        carousals1 = Carousal1.objects.all().exclude(id=c1.id)
        context['carousals1'] = carousals1
        context['c1'] = c1
        c2 = Carousal2.objects.all()[0]
        carousals2 = Carousal2.objects.all().exclude(id=c2.id)
        context['carousals2'] = carousals
        context['c2'] = c2
        c3 = Carousal3.objects.all()[0]
        carousals3 = Carousal3.objects.all().exclude(id=c3.id)
        context['carousals3'] = carousals3
        context['c3'] = c3
        lines0 = Home_description.objects.all()[0]
        context['lines0'] = lines0
        lines1 = Home_description.objects.all()[2]
        context['lines1'] = lines1
        lines2 = Home_description.objects.all()[2]
        context['lines2'] = lines2
    except:
        pass
    return render(request,'index.html',context=context)      

def home(request):        
    if request.user.is_superuser:
        recharge_total,total = 0,0
        yesterday = datetime.now()-timedelta(hours=29,minutes=30)
        users = UserProfile.objects.all()
        recharges = Paytm_history.objects.filter(TXNDATE__gte=yesterday)
        for i in recharges:
            recharge_total += float(i.TXNAMOUNT)
        noreqs = withdraw_requests.objects.filter(made_on__gte=datetime.now()-timedelta(hours=24)).filter(paid=False).count()
        for i in users:
            total += float(i.total_amount)
        context={'total':total,'recharge_total':recharge_total,'noreqs':noreqs}
    return render(request,"home.html",context=context)
                
    
def payusers(game_id,mode):
    if mode=='gold':
        game = GoldGame.objects.get(id=game_id)
    elif mode=='silver':
        game = SilverGame.objects.get(id=game_id)
    elif mode=='diamond':
        game = DiamondGame.objects.get(id=game_id)
    elif mode=='other':
        game = OtherGame.objects.get(id=game_id)
        
    #hists_for_game = History.objects.filter(id_made=game.id,paid=True,mode=mode)
    
    investment = []
    tp,tr,tg=[],[],[]
    colors = []
    res=[]                
    colors.append(float(game.red_investment))
    colors.append(float(game.purple_investment))
    colors.append(float(game.green_investment))
    investment=game.n_investment
    tr=[float(investment[i]) for i in range(len(investment)) if i%2==0]
    tp=[float(investment[i]) for i in range(len(investment)) if i==0 or float(i)==5]
    tg=[float(investment[i]) for i in range(len(investment)) if i%2!=0]
    total = 0    
    for i in colors:
        total+=i
    for i in investment:
        total+=float(i)
    game.total_investment = round(float(total),2)
    game.save()
    
    if total > 0:
    
        if tr.index(min(tr)) != 0:
            a1 = min(tr)*7 + colors[0]*2
        else:
            a1 = min(tr)*7 + colors[0]*1.5 + colors[1]*2
    
        res.append(a1)    
    
        if tg.index(min(tg)) != 2:
            a1 = min(tg)*7 + colors[2]*2
        else:
            a1 = min(tg)*7 + colors[2]*1.5 + colors[1]*2
    
        res.append(a1)                                       
    
        index_res = res.index(min(res))
    
        if index_res == 0:
            result = tr.index(min(tr))*2
            color = 'red'
            if tr.index(min(tr)) == 0: 
                color = 'red purple'
        else:
            result = tg.index(min(tg))*2+1
            color = 'green'
            if tg.index(min(tg)) == 2:
                color = 'green purple'                
        
        
        if game.result == 'unknown12':
            game.result = str(result)        
            game.color = color        
            game.save()
               
    else:  
        game.total_investment = float(random.randint(100,3000))
        game.save()
        if game.result == 'unknown12':
            result = random.randint(0,9)        
            game.result = str(result)
            if result == 0 or result == 5:
               if result == 0:                                          
                   game.color = "red purple"        
                   game.save()                                
               if result == 5:
                   game.color = "green purple"        
                   game.save() 
            else:
               if result%2 == 1:
                   game.color = "green"
                   game.save()
               else:
                   game.color = "red"
                   game.save()
    hists = History.objects.filter(id_made=game.id,paid=False,mode=mode)
    clrlst = game.color.split(' ') 
    while True:
        if '' in clrlst:
            clrlst.remove('')
        elif ' ' in clrlst:
            clrlst.remove(' ')
        else:
            break
    for i in hists:        
        i.result = "lost"
        i.color = game.color
        i.save()
        if i.color_selected:
            if i.color_selected in clrlst and game.color != 'purple':
                if game.result == '0' or game.result == '5':
                    i.user.userprofile.won = float(float(i.investment)*1.5)
                    i.user.userprofile.total_amount = float(i.user.userprofile.total_amount) + float(i.investment)*1.5
                    i.paid = True
                    i.result = "won"
                    i.wamt =  str(float(i.investment)*1.5)[:9]
                    i.save()
                    i.user.userprofile.save()                                  
                    if i.user.userprofile.refer != "False":
                        try:
                            u = User.objects.get(username=i.user.userprofile.refer)
                            up = UserProfile.objects.get(user=u)
                            if int(up.level)==4:                                
                                up.refer_income = float(up.refer_income) + float(float(i.user.userprofile.won)*0.09)
                                up.total_amount = float(up.total_amount)+float(float(i.user.userprofile.won)*0.09)
                                up.save()   
                            if up.refer != "False":                         
                                rp = User.objects.get(username=up.refer)
                                r = UserProfile.objects.get(user=rp)
                                r.refer_income2 = float(r.refer_income2) + float(float(i.user.userprofile.won)*0.06)
                                r.total_amount = float(r.total_amount)+float(float(i.user.userprofile.won)*0.06)
                                r.save()                                    
                        except:
                            pass                                                    
                else:
                    i.user.userprofile.won = float(float(i.investment)*2)
                    i.user.userprofile.total_amount = float(i.user.userprofile.total_amount) + float(float(i.investment)*2)
                    i.paid = True
                    i.result = "won"
                    i.wamt =  str(float(i.investment)*2)[:9]
                    i.save()
                    i.user.userprofile.save()                                           
                    if i.user.userprofile.refer != "False":
                        try:
                            u = User.objects.get(username=i.user.userprofile.refer)
                            up = UserProfile.objects.get(user=u)
                            if int(up.level)==4:                                
                                up.refer_income = float(up.refer_income) + float(float(i.user.userprofile.won)*0.09)
                                up.total_amount = float(up.total_amount)+float(float(i.user.userprofile.won)*0.09)
                                up.save()
                            if up.refer != "False":                         
                                rp = User.objects.get(username=up.refer)
                                r = UserProfile.objects.get(user=rp)
                                r.refer_income2 = float(r.refer_income2) + float(float(i.user.userprofile.won)*0.06)
                                r.total_amount = float(r.total_amount)+float(float(i.user.userprofile.won)*0.06)
                                r.save() 
                        except:
                            pass
            elif i.color_selected in clrlst and game.color == 'purple':
                i.user.userprofile.won = float(float(i.investment)*2)
                i.user.userprofile.total_amount = float(i.user.userprofile.total_amount) + float(float(i.investment)*2)
                i.paid = True
                i.result = "won"
                i.save()
                i.user.userprofile.save()  
                i.wamt =  str(float(i.investment)*2)[:9]
                i.save()              
                if i.user.userprofile.refer != "False":
                    try:
                        u = User.objects.get(username=i.user.userprofile.refer)
                        up = UserProfile.objects.get(user=u)
                        if int(up.level)==4:                                
                            up.refer_income = float(up.refer_income) + float(float(i.user.userprofile.won)*0.09)
                            up.total_amount = float(up.total_amount)+float(float(i.user.userprofile.won)*0.09)
                            up.save()
                        if up.refer != "False":                         
                            rp = User.objects.get(username=up.refer)
                            r = UserProfile.objects.get(user=rp)
                            r.refer_income2 = float(r.refer_income2) + float(float(i.user.userprofile.won)*0.06)
                            r.total_amount = float(r.total_amount)+float(float(i.user.userprofile.won)*0.06)
                            r.save() 
                    except:
                        pass

        if i.num_selected:
            if i.num_selected == game.result:
                i.user.userprofile.won = float(float(i.investment)*7)
                i.user.userprofile.total_amount = float(i.user.userprofile.total_amount) + float(float(i.investment)*7)
                i.paid = True 
                i.result = "won"
                i.wamt =  str(float(i.investment)*7)[:9]
                i.save()
                i.user.userprofile.save()                                                
                if i.user.userprofile.refer != "False":
                    try:
                        u = User.objects.get(username=i.user.userprofile.refer)
                        up = UserProfile.objects.get(user=u)
                        if int(up.level)==4:                                
                            up.refer_income = float(up.refer_income) + float(float(i.user.userprofile.won)*0.09)
                            up.total_amount = float(up.total_amount)+float(float(i.user.userprofile.won)*0.09)
                            up.save()                        
                        if up.refer != "False":                         
                            rp = User.objects.get(username=up.refer)
                            r = UserProfile.objects.get(user=rp)
                            r.refer_income2 = float(r.refer_income2) + float(float(i.user.userprofile.won)*0.06)
                            r.total_amount = float(r.total_amount)+float(float(i.user.userprofile.won)*0.06)
                            r.save() 
                    except:
                        pass    
 
nums = [str(0) for i in range(10)]              
 
num_for_see = [str(i) for i in range(10)]

from datetime import datetime
class NumberSection(LoginRequiredMixin,ListView):
    template_name = "gamepage.html"        
    def get(self, *args, **kwargs): 
        context = {}          
        self.gold_game = GoldGame.objects.all().order_by('-id')[0]    
        GoldGame.objects.filter(result='unknown12').exclude(id=self.gold_game.id).delete()            
        if self.gold_game.start.replace(tzinfo=utc)<=datetime.now().replace(tzinfo=utc) and self.gold_game.dec.replace(tzinfo=utc)>datetime.now().replace(tzinfo=utc):
            self.gold_started = True
            self.gold_game.status = 'accepted'  
            self.gold_game.save()      
        if self.gold_game.dec.replace(tzinfo=utc)<=datetime.now().replace(tzinfo=utc):
            self.gold_game.status = 'blocked'
            self.gold_game.save()                         
            payusers(self.gold_game.id,'gold')
        if self.gold_game.end.replace(tzinfo=utc) <= datetime.now().replace(tzinfo=utc):            
            if self.gold_game.result != 'unknown12':
                GoldGame.objects.create(mode='gold',n_investment=nums)
            else:                
                payusers(self.gold_game.id,'gold')
        x = self.gold_game.end.replace(tzinfo=utc) - datetime.now().replace(tzinfo=utc)                  
        context['gold_id'] = self.gold_game.id
        context["gold_end"] = self.gold_game.end.strftime('%M:%S')
        context["gold_minutes"],context["gold_seconds"] = (x.seconds//60)%60,x.seconds%60  
        context['gold_status'] = self.gold_game.status
        self.silver_game = SilverGame.objects.all().order_by('-id')[0]     
        SilverGame.objects.filter(result='unknown12').exclude(id=self.silver_game.id).delete()   
        if self.silver_game.start.replace(tzinfo=utc)<=datetime.now().replace(tzinfo=utc) and self.silver_game.dec.replace(tzinfo=utc)>datetime.now().replace(tzinfo=utc):
            self.silver_started = True
            self.silver_game.status = 'accepted'  
            self.silver_game.save()      
        if self.silver_game.dec.replace(tzinfo=utc)<=datetime.now().replace(tzinfo=utc):
            self.silver_game.status = 'blocked'
            self.silver_game.save()                        
            payusers(self.silver_game.id,'silver')
        if self.silver_game.end.replace(tzinfo=utc) <= datetime.now().replace(tzinfo=utc):
            if self.silver_game.result != 'unknown12':
                SilverGame.objects.create(mode='silver',n_investment=nums)
            else:                
                payusers(self.silver_game.id,'silver')
        x = self.silver_game.end.replace(tzinfo=utc) - datetime.now().replace(tzinfo=utc)                  
        context['silver_id'] = self.silver_game.id
        context["silver_end"] = self.silver_game.end.strftime('%M:%S')
        context["silver_minutes"],context["silver_seconds"] = (x.seconds//60)%60,x.seconds%60  
        context['silver_status'] = self.silver_game.status                      
        self.diamond_game = DiamondGame.objects.all().order_by('-id')[0] 
        DiamondGame.objects.filter(result='unknown12').exclude(id=self.diamond_game.id).delete()       
        if self.diamond_game.start.replace(tzinfo=utc)<=datetime.now().replace(tzinfo=utc) and self.diamond_game.dec.replace(tzinfo=utc)>datetime.now().replace(tzinfo=utc):
            self.diamond_started = True
            self.diamond_game.status = 'accepted'  
            self.diamond_game.save()      
        if self.diamond_game.dec.replace(tzinfo=utc)<=datetime.now().replace(tzinfo=utc):
            self.diamond_game.status = 'blocked'
            self.diamond_game.save()                        
            payusers(self.diamond_game.id,'diamond')
        if self.diamond_game.end.replace(tzinfo=utc) <= datetime.now().replace(tzinfo=utc):
            if self.diamond_game.result != 'unknown12':
                DiamondGame.objects.create(mode='diamond',n_investment=nums)
            else:                
                payusers(self.diamond_game.id,'diamond')
        x = self.diamond_game.end.replace(tzinfo=utc) - datetime.now().replace(tzinfo=utc)                  
        context['diamond_id'] = self.diamond_game.id
        context["diamond_end"] = self.diamond_game.end.strftime('%M:%S')
        context["diamond_minutes"],context["diamond_seconds"] = (x.seconds//60)%60,x.seconds%60  
        context['diamond_status'] = self.diamond_game.status
        self.other_game = OtherGame.objects.all().order_by('-id')[0]   
        OtherGame.objects.filter(result='unknown12').exclude(id=self.other_game.id).delete()     
        if self.other_game.start.replace(tzinfo=utc)<=datetime.now().replace(tzinfo=utc) and self.other_game.dec.replace(tzinfo=utc)>datetime.now().replace(tzinfo=utc):
            self.other_started = True
            self.other_game.status = 'accepted'  
            self.other_game.save()      
        if self.other_game.dec.replace(tzinfo=utc)<=datetime.now().replace(tzinfo=utc):
            self.other_game.status = 'blocked'
            self.other_game.save()                    
            payusers(self.other_game.id,'other')
        if self.other_game.end.replace(tzinfo=utc) <= datetime.now().replace(tzinfo=utc):
            if self.other_game.result != 'unknown12':
                OtherGame.objects.create(mode='other',n_investment=nums)
            else:                
                payusers(self.other_game.id,'other')
        x = self.other_game.end.replace(tzinfo=utc) - datetime.now().replace(tzinfo=utc)                  
        context['other_id'] = self.other_game.id
        context["other_end"] = self.other_game.end.strftime('%M:%S')
        context["other_minutes"],context["other_seconds"] = (x.seconds//60)%60,x.seconds%60  
        context['other_status'] = self.other_game.status
        gh,sh,dh,oh = GoldGame.objects.filter(mode='gold').exclude(id=self.gold_game.id).order_by('-id'),SilverGame.objects.filter(mode='silver').exclude(id=self.silver_game.id).order_by('-id'),DiamondGame.objects.filter(mode='diamond').exclude(id=self.diamond_game.id).order_by('-id'),OtherGame.objects.filter(mode='other').exclude(id=self.other_game.id).order_by('-id')
        context['gold_history'],context['silver_history'],context['diamond_history'],context['other_history']=gh,sh,dh,oh
        if gh.count()>11:
            context['gold_history'],context['silver_history'],context['diamond_history'],context['other_history']=gh[:10],sh[:10],dh[:10],oh[:10]                                                                    
        mgh,msh,mdh,moh = History.objects.filter(user=self.request.user,mode='gold').order_by('-id'),History.objects.filter(user=self.request.user,mode='silver').order_by('-id'),History.objects.filter(user=self.request.user,mode='diamond').order_by('-id'),History.objects.filter(user=self.request.user,mode='other').order_by('-id')
        context['my_gold_history'],context['my_silver_history'],context['my_diamond_history'],context['my_other_history']=mgh,msh,mdh,moh
        if mgh.count()>11:
            context['my_gold_history'],context['my_silver_history'],context['my_diamond_history'],context['my_other_history']=mgh[:10],msh[:10],mdh[:10],moh[:10]                                                                    
        return render(self.request,self.template_name,context=context)

    def post(self, *Args, **kwargs):           
        name = str(self.request.POST.get("choosen")).split(' ')
        amt = self.request.POST.get("total")
        amt1 = float(amt)
        nums = num_for_see        
        if float(amt)<10:
            messages.warning(self.request,"Investment can't be less than 10!")
            return redirect('core:play') 
        self.gold_game = GoldGame.objects.all().order_by('-id')[0]
        silver_game = SilverGame.objects.all().order_by('-id')[0]       
        diamond_game = DiamondGame.objects.all().order_by('-id')[0]       
        other_game = OtherGame.objects.all().order_by('-id')[0]               
        if float(amt) <= float(self.request.user.userprofile.total_amount):
            amt = float(amt) - float(int(amt)*0.03)
            if name[0] == 'Gold' and self.gold_game.status != "blocked":
                hist = History.objects.create(user=self.request.user)
                hist.investment = amt
                if name[1] in num_for_see: 
                    hist.num_selected = name[1]
                else:
                    hist.color_selected = name[1].lower()                                 
                hist.id_made = self.gold_game.id
                hist.mode = "gold"
                hist.save()                                
                if hist.color_selected:
                    if hist.color_selected == 'green':
                        self.gold_game.green_investment = float(self.gold_game.green_investment)+float(amt)          
                        self.gold_game.save()          
                    elif hist.color_selected == 'red':
                        self.gold_game.red_investment = float(self.gold_game.red_investment)+float(amt)
                        self.gold_game.save()                    
                    elif hist.color_selected == 'purple':
                        self.gold_game.purple_investment = float(self.gold_game.purple_investment)+float(amt)
                        self.gold_game.save()
                else:
                    index = int(hist.num_selected)
                    self.gold_game.n_investment[index] = float(self.gold_game.n_investment[index])+float(amt)
                self.gold_game.save()
                hist.save()
                self.request.user.userprofile.total_amount = float(self.request.user.userprofile.total_amount)-amt1
                self.request.user.userprofile.save()
            if name[0] == 'Silver' and silver_game.status != "blocked":
                hist = History.objects.create(user=self.request.user,investment=amt)
                hist.id_made = silver_game.id
                if name[1] in nums: 
                    hist.num_selected = name[1]                                    
                else:
                    hist.color_selected = name[1].lower() 
                hist.id_made = silver_game.id
                hist.mode = "silver"
                hist.save()                              
                if hist.color_selected:
                    if hist.color_selected == 'green':
                        silver_game.green_investment = float(silver_game.green_investment)+float(amt)                    
                    elif hist.color_selected == 'red':
                        silver_game.red_investment = float(silver_game.red_investment)+float(amt)                    
                    elif hist.color_selected == 'purple':
                        silver_game.purple_investment = float(silver_game.purple_investment)+float(amt)
                else:
                    index = int(hist.num_selected)
                    silver_game.n_investment[index] = float(silver_game.n_investment[index])+float(amt)
                silver_game.save()
                hist.save()
                self.request.user.userprofile.total_amount = float(self.request.user.userprofile.total_amount)-amt1
                self.request.user.userprofile.save()
            if name[0] == 'Diamond' and diamond_game.status != "blocked":
                hist = History.objects.create(user=self.request.user,investment=amt)
                hist.id_made = diamond_game.id
                if name[1] in nums: 
                    hist.num_selected = name[1]
                else:
                    hist.color_selected = name[1].lower() 
                hist.id_made = diamond_game.id
                hist.mode = "diamond"
                hist.save()                                
                if hist.color_selected:
                    if hist.color_selected == 'green':
                        diamond_game.green_investment = float(diamond_game.green_investment)+float(amt)                    
                    elif hist.color_selected == 'red':
                        diamond_game.red_investment = float(diamond_game.red_investment)+float(amt)                    
                    elif hist.color_selected == 'purple':
                        diamond_game.purple_investment = float(diamond_game.purple_investment)+float(amt)
                else:
                    index = int(hist.num_selected)
                    diamond_game.n_investment[index] = float(diamond_game.n_investment[index])+float(amt)
                diamond_game.save()                
                hist.save()
                self.request.user.userprofile.total_amount = float(self.request.user.userprofile.total_amount)-amt1
                self.request.user.userprofile.save()
            if name[0] == 'Other' and other_game.status != "blocked":
                hist = History.objects.create(user=self.request.user,investment=amt,)
                hist.id_made = other_game.id
                if name[1] in nums: 
                    hist.num_selected = name[1]
                else:
                    hist.color_selected = name[1].lower() 
                hist.id_made = other_game.id
                hist.mode = "other"
                hist.save()                              
                if hist.color_selected:
                    if hist.color_selected == 'green':
                        other_game.green_investment = float(other_game.green_investment)+float(amt)                    
                    elif hist.color_selected == 'red':
                        other_game.red_investment = float(other_game.red_investment)+float(amt)                    
                    elif hist.color_selected == 'purple':
                        other_game.purple_investment = float(other_game.purple_investment)+float(amt)                    
                else:
                    index = int(hist.num_selected)
                    other_game.n_investment[index] = float(other_game.n_investment[index])+float(amt)
                other_game.save()
                hist.save()
                self.request.user.userprofile.total_amount = float(self.request.user.userprofile.total_amount)-float(amt1)
                self.request.user.userprofile.save()
        else:
            messages.warning(self.request,'Insufficient balance!')
            messages.warning(self.request,format_html("{} <a href='/pay'>{}</a>", "To Recharge ","Click Here."))
        return redirect('core:play')            
