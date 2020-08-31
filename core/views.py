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
# from .models import Item, OrderItem, Order, Address, Payment, Coupon, Refund, UserProfile, Transaction, TravelDetails, ClubJoin, Paytm_order_history,Paytm_history, Carousal, Reviews, Team, Ads, Itemdealer, Myorder, Categories, Sales, CarousalClub, ReviewsImage, Contact, FAQs
from .models import History, UserProfile, Transaction, Paytm_history, NumberGame, withdraw_requests, Contact
import random
from django.shortcuts import reverse
import string
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login as auth_login
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .paytm import generate_checksum, verify_checksum
import smtplib
from django.core.paginator import Paginator
from email.message import EmailMessage
from datetime import datetime, timedelta
from django.db.models import Q
from django.db.models.functions import ( ExtractDay, ExtractHour, ExtractMinute, ExtractMonth, ExtractSecond, ExtractWeek, ExtractWeekDay, ExtractYear )
from django.utils.html import format_html


# class HomeView(ListView):
#     template_name = "home.html"
#     def get(self,*args, **kwargs):
#         items = Item.objects.all().order_by('-id')[0:7]
#         items1 = Item.objects.all().order_by('-id')[9:16]
#         items2 = Item.objects.filter(dis_per__gte=30)[0:7]
#         items3 = Item.objects.filter(dis_per__gte=30).order_by('-id')[9:16]
#         items4 = Item.objects.filter(dis_per__gte=70).order_by('-id')
#         items7 = Item.objects.filter(tag="BESTSELLER").order_by('-id')[0:7]
#         items6 = Item.objects.filter(tag="BESTSELLER")[9:16]
#         items8 = Sales.objects.filter(sale_name="DOW")
#         items11 = Sales.objects.filter(sale_name="DS")[0:7]
#         items12 = Sales.objects.filter(sale_name="DS")[9:16]
#         items9 = Sales.objects.filter(sale_name="DOD")
#         items10 = Sales.objects.filter(sale_name="FO")
#         categories = Categories.objects.all()
#         context={'object_list':items,'object_list1':items1,'cat':categories,'object_list2':items2,'object_list3':items3,'object_list4':items4,'object_list6':items6,'object_list7':items7,'object_list8':items8,'object_list9':items9,'object_list10':items10,'object_list11':items11,'object_list12':items12}
#         if datetime.now().strftime("%A")!="Sunday":
#             context["status"]="disabled"
#             context["msg"]="Wait up to SUNDAY for this sale..."
#         now = timezone.now()
#         if len(items10)>0:
#             sdate = items10[0].gold_start
#             edate = items10[0].end
#             today = datetime.today()
#             if sdate < now:
#                 context["day"]=edate.day - now.day
#                 context["hours"]=edate.hour
#                 context["minutes"]=edate.minute
#                 context["seconds"]=edate.second
#                 context["fmsg"]="Ends In"
#             else:
#                 context["day"]=-sdate.day + now.day
#                 context["hours"]=sdate.hour
#                 context["minutes"]=sdate.minute
#                 context["seconds"]=sdate.second
#                 context["fmsg"]="gold_Starts In"
#             if sdate > now:
#                 context["fstatus"]="disabled"
#         return render(self.request, self.template_name, context)
#     def post(self,*args,**kwargs):
#         if self.request.method == 'POST':
#             if self.request.POST.get('search'):
#                 query = self.request.POST.get('search')
#                 qs = Item.objects.filter(Q(title__search=query)|Q(category__search=query)|Q(descruption__search=query))
#                 msg = 'Search results'
#                 context = { 'sobs': qs , 'type':msg}
#                 if len(qs)<1:
#                     messages.info(self.request, "Invalid search")
#                     return redirect('/ecommerce/')
#             else:
#                 min_price = int(self.request.POST.get('min_price'))-int(self.request.POST.get('min_price'))*0.1
#                 max_price = int(self.request.POST.get('max_price'))+int(self.request.POST.get('max_price'))*0.1
#                 min_dis_per = int(self.request.POST.get('min_dis_price'))-int(self.request.POST.get('min_dis_price'))*0.1
#                 max_dis_per = int(self.request.POST.get('max_dis_price'))+int(self.request.POST.get('max_dis_price'))*0.1
#                 if self.request.POST.get('gold_new'):
#                     qs = Item.objects.filter(Q(dis_per__gte=min_dis_per)&Q(tag="gold_New")&Q(dis_per__lte=max_dis_per)&Q(discount_price__gte=min_price)&Q(discount_price__lte=max_price)).order_by('-id')
#                 if self.request.POST.get('bestseller'):
#                     qs = Item.objects.filter(Q(dis_per__gte=min_dis_per)&Q(tag="BESTSELLER")&Q(dis_per__lte=max_dis_per)&Q(discount_price__gte=min_price)&Q(discount_price__lte=max_price)).order_by('-id')
#                 if self.request.POST.get('bestseller') and self.request.POST.get('gold_new'):
#                     qs = Item.objects.filter(Q(dis_per__gte=min_dis_per)&Q(tag="gold_New")&Q(tag="BESTSELLER")&Q(dis_per__lte=max_dis_per)&Q(discount_price__gte=min_price)&Q(discount_price__lte=max_price)).order_by('-id')
#                 if not (self.request.POST.get('bestseller') and self.request.POST.get('gold_new')):
#                     qs = Item.objects.filter(Q(dis_per__gte=min_dis_per)&Q(dis_per__lte=max_dis_per)&Q(discount_price__gte=min_price)&Q(discount_price__lte=max_price)).order_by('-id')
#                 if len(qs)>36:
#                     qs = qs[0:36]
#                 msg = 'Filter results'
#                 context = { 'sobs': qs , 'type':msg}
#             return render(self.request, 'search.html', context=context)
            
# class travels(ListView):
#     model = TravelDetails
#     template_name = "travels.html"
#     def post(self,*args,**kwargs):
#         if self.request.method == 'POST':
#             travel_details = TravelDetails.objects.create(
#                 name = self.request.POST.get('name'),
#                 spoint = self.request.POST.get('spoint'),
#                 epoint = self.request.POST.get('epoint'),
#                 phonenumber = self.request.POST.get('phonenumber')
#             )
#             travel_details.email = self.request.POST.get('email')
#             travel_details.carmodel = self.request.POST.get('carmodel')
#             travel_details.carcapacity = self.request.POST.get('carcapacity')
#             travel_details.save()
#             messages.info(self.request,'We will contact you soon about travel details. Thank you')
#             return redirect('core:home')
#         return render(self.request,self.template_name)


def refgenrator(name):
    l=random.choices(string.ascii_lowercase+string.ascii_uppercase,k=6)
    c=""
    for i in range(len(l)):
        c+=chr(l[i])
    return str(c)

def privacy(request):
    return render(request,"privacy.html")
            
    
# def sitemap(request):
#     return render(request, 'sitemap.xml')

# def robots(request):
#     return render(request, 'robots.txt')
    

# @login_required
# def refund(request, slug):
#     myorderitem = get_object_or_404(Item, slug=slug)
#     myorders = Myorder.objects.get(user=request.user, item=myorderitem, status='404')
#     myorders.status = '200'
#     myorders.save()
#     server = smtplib.SMTP_SSL('smtp.gmail.com',465)
#     server.login('presimaxinfo@gmail.com','Mama_presimax_bagundi') 
#     msg = EmailMessage()
#     recupients = ['hemanthraju9966@gmail.com', 'navi87362@gmail.com']
#     msg.set_content("This is a computer generated email, don't reply to this mail.\n"+ str(request.user.username) +" has request refund for item with name" + str(myorderitem.title) + "and amount with shuppping charges Rs. "+str(myorderitem.schargeinc))
#     msg['Subject'] = 'Order Cancellation'
#     msg['From'] = "presimaxinfo@gmail.com"
#     msg['To'] = ", ".join(recupients)
#     server.send_message(msg)
#     msg1 = EmailMessage()
#     msg1.set_content("This is a computer generated email, don't reply to this mail.\n This mail is to confirm your order cancellation for "+  str(myorderitem.title)+" on PRESIMAX of Rs." + str(myorderitem.schargeinc) + " \nIf you want refund then please contact to +91 94932 59030 else refund is not processed.")
#     msg1['Subject'] = 'Order Cancellation'
#     msg1['From'] = "presimaxinfo@gmail.com"
#     msg1['To'] = request.user.email
#     server.send_message(msg1)
#     server.quit()
#     return redirect("core:myorders")

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
        if recharges.count()>10:
            context['withdrawls'] = withdrawls[:10]
        refers = UserProfile.objects.filter(refer=self.request.user.username).order_by('-id')
        context['refers'] = refers
        if refers.count()>10: 
            context['refers'] = refers[:10]
        return render(self.request,self.template_name,context=context)
    def post(self, *args, **kwargs):
        if self.request.method == 'POST':            
            if self.request.FILES.get('image'):
                self.request.user.userprofile.userphoto = self.request.FILES.get('image')
                self.request.user.userprofile.save()
            if (len(self.request.POST.get('pnumber'))>9 and len(self.request.POST.get('pnumber'))<20): 
                self.request.user.userprofile.phone_number = self.request.POST.get('pnumber')
            if len(self.request.POST.get('uname'))>0:
                self.request.user.username = self.request.POST.get('uname')
                self.request.user.save()
            if len(self.request.user.email)>0:
                self.request.user.email = self.request.POST.get('email')
                self.request.user.save()    

            if (len(self.request.POST.get('upiid'))>5 and len(self.request.POST.get('upiid'))<25) and int(self.request.POST.get('amt'))>100 and float(self.request.user.userprofile.total_amount)>=int(self.request.POST.get('amt')): 
                withdraw_request = withdraw_requests.objects.create(amount=str(self.request.POST.get('amt')),UPIID=self.request.POST.get('upiid'),user=self.request.user)                
            elif not (len(self.request.POST.get('upiid'))>5 and len(self.request.POST.get('upiid'))<25) and int(self.request.POST.get('amt'))>100:
                messages.warning(self.request,'Invalid details entered.')
            if not float(self.request.user.userprofile.total_amount)>=int(self.request.POST.get('amt')): 
                messages.warning(self.request,'Insufficient balance in your wallet.')
            context={}
            return render(self.request,self.template_name,context=context)

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

def create_time_modules(add_delta = 0):                
    delta = timedelta(seconds=add_delta)
    start = datetime.now() + delta
    end = start + timedelta(minutes = 3,seconds=30)
    buffer = start + timedelta(minutes = 3,seconds=35)
    new = start + timedelta(minutes = 3,seconds=58)
    correct = start + timedelta(minutes = 4)
    return end,buffer,new,correct,start

class Gold_game:
    def __init__(self,name,delta=0):
        self.name = name
        self.delta = delta    

    def running_game(self,repeat=1):                        
        self.end,self.buffer,self.new,self.correct,self.start = create_time_modules(add_delta=self.delta)
        # self.status = True
        self.game = NumberGame.objects.create(mode=self.name)    
        self.game.n_investment = [str(0) for i in range(10)]    
        self.status = 'accepted'
        self.created =True
        self.rest = False
        self.game.save()
        
    def result(self):

        if self.created:          
            if self.end<=datetime.now() and self.new >datetime.now():
                self.rest = False
                self.status = 'blocked'            
        if not self.rest:
            if self.buffer<=datetime.now():
                self.rest = True
                investment = []
                tp,tr,tg=[],[],[]
                colors = []
                res=[]
                # tp.append(int(self.game.purple_investment))
                # tr.append(int(self.game.red_investment))
                # tg.append(int(self.game.green_investment))
                colors.append(float(self.game.red_investment))
                colors.append(float(self.game.purple_investment))
                colors.append(float(self.game.green_investment))
                investment=self.game.n_investment
                tr=[float(investment[i]) for i in range(len(investment)) if float(i)%2==0]
                tp=[float(investment[i]) for i in range(len(investment)) if float(i)==0 or float(i)==5]
                tg=[float(investment[i]) for i in range(len(investment)) if float(i)%2!=0]
                total = 0
                for i in colors:
                    total+=i
                for i in investment:
                    total+=float(i)
                self.game.total_investment = round(float(total),2)
                self.game.save()
                if tr.index(min(tr)) != 0:
                    a1 = min(tr)*7 + colors[0]*2
                else:
                    a1 = min(tr)*7 + colors[0]*1.5 + colors[1]*4.5

                res.append(a1)    

                if tg.index(min(tg)) != 2:
                    a1 = min(tg)*7 + colors[2]*2
                else:
                    a1 = min(tg)*7 + colors[2]*1.5 + colors[1]*4.5

                res.append(a1)                                       

                index_res = res.index(min(res))

                if index_res == 0:
                    result = tr.index(min(tr))*2
                    color = 'red'
                    if tr.index(min(tr)) != 0:
                        color = 'red purple'
                else:
                    result = tg.index(min(tg))*2+1
                    color = 'green'
                    if tg.index(min(tg)) != 2:
                        color = 'green purple'                
                
                if self.game.result == 'unknown':
                    self.game.result = str(result)        
                    self.game.color = color        
                    self.game.save()                

                hists = History.objects.filter(id_made=self.game.id,paid=True)
                clrlst = self.game.color.split(' ')
                while True:
                    if '' in clrlst:
                        clrlst.remove('')
                    elif ' ' in clrlst:
                        clrlst.remove(' ')
                    else:
                        break
                for i in hists:
                    if i.color_selected:
                        if i.color_selected in clrlst and self.game.color != 'purple':
                            if self.game.result == '0' or self.game.result == '5':
                                i.user.won = float(investment*1.5)
                                i.user.total_amount = float(i.user.total_amount) + float(i.user.won)+float(investment)
                                i.paid = True
                                i.user.save()
                                i.save()
                                if i.user.refer != "False":
                                    u = User.objects.get(username=i.user.refer)
                                    up = UserProfile.objects.get(user=u)
                                    up.refer_income = float(up.refer_income) + float(float(i.user.won)*0.75)
                                    up.total_amount = float(up.total_amount)+float(float(i.user.won)*0.75)
                                    up.save()
                            else:
                                i.user.won = float(investment*2)
                                i.user.total_amount = float(i.user.total_amount) + float(i.user.won)+float(investment)
                                i.paid = True
                                i.user.save()
                                i.save()
                                if i.user.refer != "False":
                                    u = User.objects.get(username=i.user.refer)
                                    up = UserProfile.objects.get(user=u)
                                    up.refer_income = float(up.refer_income) + float(float(i.user.won)*0.75)
                                    up.total_amount = float(up.total_amount)+float(float(i.user.won)*0.75)
                                    up.save()
                        elif i.color_selected in clrlst and self.game.color == 'purple':
                            i.user.won = float(investment*4.5)
                            i.user.total_amount = float(i.user.total_amount) + float(i.user.won)+float(investment)
                            i.paid = True
                            i.user.save()
                            i.save()
                            if i.user.refer != "False":
                                u = User.objects.get(username=i.user.refer)
                                up = UserProfile.objects.get(user=u)
                                up.refer_income = float(up.refer_income) + float(float(i.user.won)*0.75)
                                up.total_amount = float(up.total_amount)+float(float(i.user.won)*0.75)
                                up.save()

                    if i.num_selected:
                        if i.num_selected == self.game.result:
                            i.user.won = float(investment*7)
                            i.user.total_amount = float(i.user.total_amount) + float(i.user.won)+float(investment)
                            i.paid = True
                            i.user.save()
                            i.save()
                            if i.user.refer != "False":
                                u = User.objects.get(username=i.user.refer)
                                up = UserProfile.objects.get(user=u)
                                up.refer_income = float(up.refer_income) + float(float(i.user.won)*0.75)
                                up.total_amount = float(up.total_amount)+float(float(i.user.won)*0.75)
                                up.save()

        if self.rest and self.game.result != 'unknown':
            if self.new<=datetime.now():
                self.created = False
                # print('back')
                return self.running_game()
                    
    def timer(self):
        x = self.correct - datetime.now()          
        minutes=(x.seconds//60)%60
        seconds=x.seconds%60
        return minutes,seconds

class Silver_game:
    def __init__(self,name,delta=0):
        self.name = name
        self.delta = delta    

    def running_game(self,repeat=1):                        
        self.end,self.buffer,self.new,self.correct,self.start = create_time_modules(add_delta=self.delta)
        # self.status = True
        self.game = NumberGame.objects.create(mode=self.name)    
        self.game.n_investment = [str(0) for i in range(10)]    
        self.status = 'accepted'
        self.created =True
        self.rest = False
        self.game.save()
        
    def result(self):

        if self.created:          
            if self.end<=datetime.now() and self.new >datetime.now():
                self.rest = False
                self.status = 'blocked'            
        if not self.rest:
            if self.buffer<=datetime.now():
                self.rest = True
                investment = []
                tp,tr,tg=[],[],[]
                colors = []
                res=[]
                # tp.append(int(self.game.purple_investment))
                # tr.append(int(self.game.red_investment))
                # tg.append(int(self.game.green_investment))
                colors.append(float(self.game.red_investment))
                colors.append(float(self.game.purple_investment))
                colors.append(float(self.game.green_investment))
                investment=self.game.n_investment
                tr=[float(investment[i]) for i in range(len(investment)) if float(i)%2==0]
                tp=[float(investment[i]) for i in range(len(investment)) if float(i)==0 or float(i)==5]
                tg=[float(investment[i]) for i in range(len(investment)) if float(i)%2!=0]
                total = 0
                for i in colors:
                    total+=i
                for i in investment:
                    total+=float(i)
                self.game.total_investment = round(float(total),2)
                self.game.save()
                if tr.index(min(tr)) != 0:
                    a1 = min(tr)*7 + colors[0]*2
                else:
                    a1 = min(tr)*7 + colors[0]*1.5 + colors[1]*4.5

                res.append(a1)    

                if tg.index(min(tg)) != 2:
                    a1 = min(tg)*7 + colors[2]*2
                else:
                    a1 = min(tg)*7 + colors[2]*1.5 + colors[1]*4.5

                res.append(a1)                                       

                index_res = res.index(min(res))

                if index_res == 0:
                    result = tr.index(min(tr))*2
                    color = 'red'
                    if tr.index(min(tr)) != 0:
                        color = 'red purple'
                else:
                    result = tg.index(min(tg))*2+1
                    color = 'green'
                    if tg.index(min(tg)) != 2:
                        color = 'green purple'                
                
                if self.game.result == 'unknown':
                    self.game.result = str(result)        
                    self.game.color = color        
                    self.game.save()                

                hists = History.objects.filter(id_made=self.game.id,paid=True)
                clrlst = self.game.color.split(' ')
                while True:
                    if '' in clrlst:
                        clrlst.remove('')
                    elif ' ' in clrlst:
                        clrlst.remove(' ')
                    else:
                        break
                for i in hists:
                    if i.color_selected:
                        if i.color_selected in clrlst and self.game.color != 'purple':
                            if self.game.result == '0' or self.game.result == '5':
                                i.user.won = float(investment*1.5)
                                i.user.total_amount = float(i.user.total_amount) + float(i.user.won)+float(investment)
                                i.paid = True
                                i.user.save()
                                i.save()
                                if i.user.refer != "False":
                                    u = User.objects.get(username=i.user.refer)
                                    up = UserProfile.objects.get(user=u)
                                    up.refer_income = float(up.refer_income) + float(float(i.user.won)*0.75)
                                    up.total_amount = float(up.total_amount)+float(float(i.user.won)*0.75)
                                    up.save()
                            else:
                                i.user.won = float(investment*2)
                                i.user.total_amount = float(i.user.total_amount) + float(i.user.won)+float(investment)
                                i.paid = True
                                i.user.save()
                                i.save()
                                if i.user.refer != "False":
                                    u = User.objects.get(username=i.user.refer)
                                    up = UserProfile.objects.get(user=u)
                                    up.refer_income = float(up.refer_income) + float(float(i.user.won)*0.75)
                                    up.total_amount = float(up.total_amount)+float(float(i.user.won)*0.75)
                                    up.save()
                        elif i.color_selected in clrlst and self.game.color == 'purple':
                            i.user.won = float(investment*4.5)
                            i.user.total_amount = float(i.user.total_amount) + float(i.user.won)+float(investment)
                            i.paid = True
                            i.user.save()
                            i.save()
                            if i.user.refer != "False":
                                u = User.objects.get(username=i.user.refer)
                                up = UserProfile.objects.get(user=u)
                                up.refer_income = float(up.refer_income) + float(float(i.user.won)*0.75)
                                up.total_amount = float(up.total_amount)+float(float(i.user.won)*0.75)
                                up.save()

                    if i.num_selected:
                        if i.num_selected == self.game.result:
                            i.user.won = float(investment*7)
                            i.user.total_amount = float(i.user.total_amount) + float(i.user.won)+float(investment)
                            i.paid = True
                            i.user.save()
                            i.save()
                            if i.user.refer != "False":
                                u = User.objects.get(username=i.user.refer)
                                up = UserProfile.objects.get(user=u)
                                up.refer_income = float(up.refer_income) + float(float(i.user.won)*0.75)
                                up.total_amount = float(up.total_amount)+float(float(i.user.won)*0.75)
                                up.save()

        if self.rest and self.game.result != 'unknown':
            if self.new<=datetime.now():
                self.created = False
                # print('back')
                return self.running_game()
                    
    def timer(self):
        x = self.correct - datetime.now()          
        minutes=(x.seconds//60)%60
        seconds=x.seconds%60
        return minutes,seconds

class Diamond_game:
    def __init__(self,name,delta=0):
        self.name = name
        self.delta = delta    

    def running_game(self,repeat=1):                        
        self.end,self.buffer,self.new,self.correct,self.start = create_time_modules(add_delta=self.delta)
        # self.status = True
        self.game = NumberGame.objects.create(mode=self.name)    
        self.game.n_investment = [str(0) for i in range(10)]    
        self.status = 'accepted'
        self.created =True
        self.rest = False
        self.game.save()
        
    def result(self):

        if self.created:          
            if self.end<=datetime.now() and self.new >datetime.now():
                self.rest = False
                self.status = 'blocked'            
        if not self.rest:
            if self.buffer<=datetime.now():
                self.rest = True
                investment = []
                tp,tr,tg=[],[],[]
                colors = []
                res=[]
                # tp.append(int(self.game.purple_investment))
                # tr.append(int(self.game.red_investment))
                # tg.append(int(self.game.green_investment))
                colors.append(float(self.game.red_investment))
                colors.append(float(self.game.purple_investment))
                colors.append(float(self.game.green_investment))
                investment=self.game.n_investment
                tr=[float(investment[i]) for i in range(len(investment)) if float(i)%2==0]
                tp=[float(investment[i]) for i in range(len(investment)) if float(i)==0 or float(i)==5]
                tg=[float(investment[i]) for i in range(len(investment)) if float(i)%2!=0]
                total = 0
                for i in colors:
                    total+=i
                for i in investment:
                    total+=float(i)
                self.game.total_investment = round(float(total),2)
                self.game.save()
                if tr.index(min(tr)) != 0:
                    a1 = min(tr)*7 + colors[0]*2
                else:
                    a1 = min(tr)*7 + colors[0]*1.5 + colors[1]*4.5

                res.append(a1)    

                if tg.index(min(tg)) != 2:
                    a1 = min(tg)*7 + colors[2]*2
                else:
                    a1 = min(tg)*7 + colors[2]*1.5 + colors[1]*4.5

                res.append(a1)                                       

                index_res = res.index(min(res))

                if index_res == 0:
                    result = tr.index(min(tr))*2
                    color = 'red'
                    if tr.index(min(tr)) != 0:
                        color = 'red purple'
                else:
                    result = tg.index(min(tg))*2+1
                    color = 'green'
                    if tg.index(min(tg)) != 2:
                        color = 'green purple'                
                
                if self.game.result == 'unknown':
                    self.game.result = str(result)        
                    self.game.color = color        
                    self.game.save()                

                hists = History.objects.filter(id_made=self.game.id,paid=True)
                clrlst = self.game.color.split(' ')
                while True:
                    if '' in clrlst:
                        clrlst.remove('')
                    elif ' ' in clrlst:
                        clrlst.remove(' ')
                    else:
                        break
                for i in hists:
                    if i.color_selected:
                        if i.color_selected in clrlst and self.game.color != 'purple':
                            if self.game.result == '0' or self.game.result == '5':
                                i.user.won = float(investment*1.5)
                                i.user.total_amount = float(i.user.total_amount) + float(i.user.won)+float(investment)
                                i.paid = True
                                i.user.save()
                                i.save()
                                if i.user.refer != "False":
                                    u = User.objects.get(username=i.user.refer)
                                    up = UserProfile.objects.get(user=u)
                                    up.refer_income = float(up.refer_income) + float(float(i.user.won)*0.75)
                                    up.total_amount = float(up.total_amount)+float(float(i.user.won)*0.75)
                                    up.save()
                            else:
                                i.user.won = float(investment*2)
                                i.user.total_amount = float(i.user.total_amount) + float(i.user.won)+float(investment)
                                i.paid = True
                                i.user.save()
                                i.save()
                                if i.user.refer != "False":
                                    u = User.objects.get(username=i.user.refer)
                                    up = UserProfile.objects.get(user=u)
                                    up.refer_income = float(up.refer_income) + float(float(i.user.won)*0.75)
                                    up.total_amount = float(up.total_amount)+float(float(i.user.won)*0.75)
                                    up.save()
                        elif i.color_selected in clrlst and self.game.color == 'purple':
                            i.user.won = float(investment*4.5)
                            i.user.total_amount = float(i.user.total_amount) + float(i.user.won)+float(investment)
                            i.paid = True
                            i.user.save()
                            i.save()
                            if i.user.refer != "False":
                                u = User.objects.get(username=i.user.refer)
                                up = UserProfile.objects.get(user=u)
                                up.refer_income = float(up.refer_income) + float(float(i.user.won)*0.75)
                                up.total_amount = float(up.total_amount)+float(float(i.user.won)*0.75)
                                up.save()

                    if i.num_selected:
                        if i.num_selected == self.game.result:
                            i.user.won = float(investment*7)
                            i.user.total_amount = float(i.user.total_amount) + float(i.user.won)+float(investment)
                            i.paid = True
                            i.user.save()
                            i.save()
                            if i.user.refer != "False":
                                u = User.objects.get(username=i.user.refer)
                                up = UserProfile.objects.get(user=u)
                                up.refer_income = float(up.refer_income) + float(float(i.user.won)*0.75)
                                up.total_amount = float(up.total_amount)+float(float(i.user.won)*0.75)
                                up.save()

        if self.rest and self.game.result != 'unknown':
            if self.new<=datetime.now():
                self.created = False
                # print('back')
                return self.running_game()
                    
    def timer(self):
        x = self.correct - datetime.now()          
        minutes=(x.seconds//60)%60
        seconds=x.seconds%60
        return minutes,seconds

class Other_game:
    def __init__(self,name,delta=0):
        self.name = name
        self.delta = delta    

    def running_game(self,repeat=1):                        
        self.end,self.buffer,self.new,self.correct,self.start = create_time_modules(add_delta=self.delta)
        # self.status = True
        self.game = NumberGame.objects.create(mode=self.name)    
        self.game.n_investment = [str(0) for i in range(10)]    
        self.status = 'accepted'
        self.created =True
        self.rest = False
        self.game.save()
        
    def result(self):

        if self.created:          
            if self.end<=datetime.now() and self.new >datetime.now():
                self.rest = False
                self.status = 'blocked'            
        if not self.rest:
            if self.buffer<=datetime.now():
                self.rest = True
                investment = []
                tp,tr,tg=[],[],[]
                colors = []
                res=[]
                # tp.append(int(self.game.purple_investment))
                # tr.append(int(self.game.red_investment))
                # tg.append(int(self.game.green_investment))
                colors.append(float(self.game.red_investment))
                colors.append(float(self.game.purple_investment))
                colors.append(float(self.game.green_investment))
                investment=self.game.n_investment
                tr=[float(investment[i]) for i in range(len(investment)) if float(i)%2==0]
                tp=[float(investment[i]) for i in range(len(investment)) if float(i)==0 or float(i)==5]
                tg=[float(investment[i]) for i in range(len(investment)) if float(i)%2!=0]
                total = 0
                for i in colors:
                    total+=i
                for i in investment:
                    total+=float(i)
                self.game.total_investment = round(float(total),2)
                self.game.save()
                if tr.index(min(tr)) != 0:
                    a1 = min(tr)*7 + colors[0]*2
                else:
                    a1 = min(tr)*7 + colors[0]*1.5 + colors[1]*4.5

                res.append(a1)    

                if tg.index(min(tg)) != 2:
                    a1 = min(tg)*7 + colors[2]*2
                else:
                    a1 = min(tg)*7 + colors[2]*1.5 + colors[1]*4.5

                res.append(a1)                                       

                index_res = res.index(min(res))

                if index_res == 0:
                    result = tr.index(min(tr))*2
                    color = 'red'
                    if tr.index(min(tr)) != 0:
                        color = 'red purple'
                else:
                    result = tg.index(min(tg))*2+1
                    color = 'green'
                    if tg.index(min(tg)) != 2:
                        color = 'green purple'                
                
                if self.game.result == 'unknown':
                    self.game.result = str(result)        
                    self.game.color = color        
                    self.game.save()                

                hists = History.objects.filter(id_made=self.game.id,paid=True)
                clrlst = self.game.color.split(' ')
                while True:
                    if '' in clrlst:
                        clrlst.remove('')
                    elif ' ' in clrlst:
                        clrlst.remove(' ')
                    else:
                        break
                for i in hists:
                    if i.color_selected:
                        if i.color_selected in clrlst and self.game.color != 'purple':
                            if self.game.result == '0' or self.game.result == '5':
                                i.user.won = float(investment*1.5)
                                i.user.total_amount = float(i.user.total_amount) + float(i.user.won)+float(investment)
                                i.paid = True
                                i.user.save()
                                i.save()
                                if i.user.refer != "False":
                                    u = User.objects.get(username=i.user.refer)
                                    up = UserProfile.objects.get(user=u)
                                    up.refer_income = float(up.refer_income) + float(float(i.user.won)*0.75)
                                    up.total_amount = float(up.total_amount)+float(float(i.user.won)*0.75)
                                    up.save()
                            else:
                                i.user.won = float(investment*2)
                                i.user.total_amount = float(i.user.total_amount) + float(i.user.won)+float(investment)
                                i.paid = True
                                i.user.save()
                                i.save()
                                if i.user.refer != "False":
                                    u = User.objects.get(username=i.user.refer)
                                    up = UserProfile.objects.get(user=u)
                                    up.refer_income = float(up.refer_income) + float(float(i.user.won)*0.75)
                                    up.total_amount = float(up.total_amount)+float(float(i.user.won)*0.75)
                                    up.save()
                        elif i.color_selected in clrlst and self.game.color == 'purple':
                            i.user.won = float(investment*4.5)
                            i.user.total_amount = float(i.user.total_amount) + float(i.user.won)+float(investment)
                            i.paid = True
                            i.user.save()
                            i.save()
                            if i.user.refer != "False":
                                u = User.objects.get(username=i.user.refer)
                                up = UserProfile.objects.get(user=u)
                                up.refer_income = float(up.refer_income) + float(float(i.user.won)*0.75)
                                up.total_amount = float(up.total_amount)+float(float(i.user.won)*0.75)
                                up.save()

                    if i.num_selected:
                        if i.num_selected == self.game.result:
                            i.user.won = float(investment*7)
                            i.user.total_amount = float(i.user.total_amount) + float(i.user.won)+float(investment)
                            i.paid = True
                            i.user.save()
                            i.save()
                            if i.user.refer != "False":
                                u = User.objects.get(username=i.user.refer)
                                up = UserProfile.objects.get(user=u)
                                up.refer_income = float(up.refer_income) + float(float(i.user.won)*0.75)
                                up.total_amount = float(up.total_amount)+float(float(i.user.won)*0.75)
                                up.save()

        if self.rest and self.game.result != 'unknown':
            if self.new<=datetime.now():
                self.created = False
                # print('back')
                return self.running_game()
                    
    def timer(self):
        x = self.correct - datetime.now()          
        minutes=(x.seconds//60)%60
        seconds=x.seconds%60
        return minutes,seconds

gold_game = Gold_game('gold')
gold_game.running_game()
silver_game = Silver_game('silver')
silver_game.running_game()
diamond_game = Diamond_game('diamond')
diamond_game.running_game()
other_game = Other_game('other')
other_game.running_game()

nums = [str(i) for i in range(10)]

class NumberSection(LoginRequiredMixin,ListView):
    template_name = "gamepage.html"        
    def get(self, *args, **kwargs):
        context = {}                
        gold_game.result()
        silver_game.result()
        diamond_game.result()
        other_game.result()
        gh,sh,dh,oh = NumberGame.objects.filter(mode='gold').order_by('-id'),NumberGame.objects.filter(mode='silver').order_by('-id'),NumberGame.objects.filter(mode='diamond').order_by('-id'),NumberGame.objects.filter(mode='other').order_by('-id')
        context['gold_history'],context['silver_history'],context['diamond_history'],context['other_history']=gh,sh,dh,oh
        if gh.count()>11:
            context['gold_history'],context['silver_history'],context['diamond_history'],context['other_history']=gh[:10],sh[:10],dh[:10],oh[:10]
        context['gold_id'] = gold_game.game.id
        context['silver_id'] = silver_game.game.id
        context['diamond_id'] = diamond_game.game.id
        context['other_id'] = other_game.game.id
        context['gold_status'],context['silver_status'],context['diamond_status'],context['other_status'] = gold_game.status,silver_game.status,diamond_game.status,other_game.status    
        context["gold_minutes"],context["gold_seconds"] = gold_game.timer()
        context["silver_minutes"],context["silver_seconds"] = silver_game.timer()
        context["other_minutes"],context["other_seconds"] = other_game.timer()
        context["diamond_minutes"],context["diamond_seconds"] = diamond_game.timer()
        return render(self.request,self.template_name,context=context)

    def post(self, *Args, **kwargs):        
        name = str(self.request.POST.get("choosen")).split(' ')
        amt = self.request.POST.get("total")
        amt1 = float(amt)
        # prfloat(amt)
        if float(amt) <= float(self.request.user.userprofile.total_amount):
            amt = float(amt) - float(int(amt)*0.03)
            if name[0] == 'Gold' and gold_game.status != "blocked":

                hist = History.objects.create(user=self.request.user)
                hist.investment = amt
                if name[1] in nums: 
                    hist.num_selected = name[1]
                else:
                    hist.color_selected = name[1].lower()                                 
                hist.id_made = gold_game.game.id
                hist.save()
                hist.paid = True                
                if hist.color_selected:
                    if hist.color_selected == 'green':
                        gold_game.game.green_investment = float(gold_game.game.green_investment)+float(amt)                    
                    elif hist.color_selected == 'red':
                        gold_game.game.red_investment = float(gold_game.game.red_investment)+float(amt)                    
                    elif hist.color_selected == 'purple':
                        gold_game.game.purple_investment = float(gold_game.game.purple_investment)+float(amt)
                else:
                    index = int(hist.num_selected)-1
                    gold_game.game.n_investment[index] = int(gold_game.game.n_investment[index])+float(amt)
                gold_game.game.save()
                hist.save()
                self.request.user.userprofile.total_amount = float(self.request.user.userprofile.total_amount)-amt1
                self.request.user.userprofile.save()
            if name[0] == 'Silver' and silver_game.status != "blocked":
                hist = History.objects.create(user=self.request.user,investment=amt)
                hist.id_made = silver_game.game.id
                if name[1] in nums: 
                    hist.num_selected = name[1]                                    
                else:
                    hist.color_selected = name[1].lower() 
                hist.save()
                hist.paid = True                
                if hist.color_selected:
                    if hist.color_selected == 'green':
                        silver_game.game.green_investment = float(silver_game.game.green_investment)+float(amt)                    
                    elif hist.color_selected == 'red':
                        silver_game.game.red_investment = float(silver_game.game.red_investment)+float(amt)                    
                    elif hist.color_selected == 'purple':
                        silver_game.game.purple_investment = float(silver_game.game.purple_investment)+float(amt)
                else:
                    index = int(hist.num_selected)-1
                    silver_game.game.n_investment[index] = float(silver_game.game.n_investment[index])+float(amt)
                silver_game.game.save()
                hist.save()
                self.request.user.userprofile.total_amount = float(self.request.user.userprofile.total_amount)-amt1
                self.request.user.userprofile.save()
            if name[0] == 'Diamond' and diamond_game.status != "blocked":
                hist = History.objects.create(user=self.request.user,investment=amt)
                hist.id_made = diamond_game.game.id
                if name[1] in nums: 
                    hist.num_selected = name[1]
                else:
                    hist.color_selected = name[1].lower() 
                hist.save()
                hist.paid = True                
                if hist.color_selected:
                    if hist.color_selected == 'green':
                        diamond_game.game.green_investment = float(diamond_game.game.green_investment)+float(amt)                    
                    elif hist.color_selected == 'red':
                        diamond_game.game.red_investment = float(diamond_game.game.red_investment)+float(amt)                    
                    elif hist.color_selected == 'purple':
                        diamond_game.game.purple_investment = float(diamond_game.game.purple_investment)+float(amt)
                else:
                    index = int(hist.num_selected)-1
                    diamond_game.game.n_investment[index] = float(diamond_game.game.n_investment[index])+float(amt)
                diamond_game.game.save()
                hist.save()
                self.request.user.userprofile.total_amount = float(self.request.user.userprofile.total_amount)-amt1
                self.request.user.userprofile.save()
            if name[0] == 'Other' and other_game.status != "blocked":
                hist = History.objects.create(user=self.request.user,investment=amt,)
                hist.id_made = other_game.game.id
                if name[1] in nums: 
                    hist.num_selected = name[1]
                else:
                    hist.color_selected = name[1].lower() 
                hist.save()
                hist.paid = True                
                if hist.color_selected:
                    if hist.color_selected == 'green':
                        other_game.game.green_investment = float(other_game.game.green_investment)+float(amt)                    
                    elif hist.color_selected == 'red':
                        other_game.game.red_investment = float(other_game.game.red_investment)+float(amt)                    
                    elif hist.color_selected == 'purple':
                        other_game.game.purple_investment = float(other_game.game.purple_investment)+float(amt)                    
                else:
                    index = int(hist.num_selected)-1
                    other_game.game.n_investment[index] = float(other_game.game.n_investment[index])+float(amt)
                other_game.game.save()
                hist.save()
                self.request.user.userprofile.total_amount = float(self.request.user.userprofile.total_amount)-float(amt1)
                self.request.user.userprofile.save()
        else:
            messages.warning(self.request,'Insufficient balance!')
            messages.warning(self.request,format_html("{} <a href='/pay'>{}</a>", "To Recharge ","Click Here."))
        return redirect('core:play')
            

@login_required
def payment(request):
    if request.method == "GET":
        return render(request, 'payments.html')
    if request.method == "POST":
        try:
            amt = request.POST.get('amt')
            if not float(amt)>100:
                messages.info(request,'Amount should be greater than Rs.100')    
                return render(request, 'payments.html')
        except:
            messages.info(request,'Enter Valid amount')
            return render(request, 'payments.html')
        transaction = Transaction.objects.create(made_by=request.user, amount=amt)
        transaction.save()
        merchant_key = settings.PAYTM_SECRET_KEY

        params = (
            ('MID', settings.PAYTM_MERCHANT_ID),
            ('ORDER_ID', str(transaction.order_id)),
            ('CUST_ID', str(transaction.made_by.email)),
            ('TXN_AMOUNT', str(transaction.amount)),
            ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
            ('WEBSITE', settings.PAYTM_WEBSITE),
            # ('EMAIL', request.user.email),
            # ('MOBILE_N0', '9911223388'),
            ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
            ('CALLBACK_URL', 'http://localhost:8000/callback/'),
            ('MERC_UNQ_REF', str(request.user.id)),
            # ('PAYMENT_MODE_ONLY', 'NO'),
        )

        paytm_params = dict(params)
        checksum = generate_checksum(paytm_params, merchant_key)

        transaction.checksum = checksum
        transaction.save()

        paytm_params['CHECKSUMHASH'] = checksum
        print('SENT: ', checksum)
        return render(request, 'redirect.html', context=paytm_params)

@csrf_exempt
def callback(request):
    if request.method == "POST":
        user = request.user
        MERCHANT_KEY = settings.PAYTM_SECRET_KEY
        data_dict = {}
        data_dict = dict(request.POST.items())

        verify = verify_checksum(data_dict, MERCHANT_KEY, data_dict['CHECKSUMHASH'])             #verifing checksum
        if verify:
            for key in request.POST:                                                                      #converting string to float
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
            return render(request, "callback.html", {"paytm":data_dict})
            if not data_dict['STATUS'] == 'TXN_SUCCESS':                                
                up.total_amount = float(up.total_amount) + float(data_dict['TXNAMOUNT'])
                up.save()
        else:
            return HttpResponse("checksum verify failed")
    return HttpResponse(status=200)

	
def signup(self, request, user): 	
    # url = self.request.get_full_path()
    # lst = url.split("/")[-1]    	    				    
    user.first_name = self.cleaned_data['first_name']
    user.last_name = self.cleaned_data['last_name'] 
    user.save()     
    return user     

def index(request):
    return render(request,'index.html')