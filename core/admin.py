from django.contrib import admin

# from .models import Item, OrderItem, Order, Payment, Coupon, Refund, Address, UserProfile, Transaction, TravelDetails, Paytm_history, Paytm_order_history, ClubJoin, Carousal, Sizes_class, Reviews, Team, Ads, Itemimage, Itemdealer, Myorder, Sales, Categories, Extrasales, CarousalClub, ReviewsImage, Contact, FAQs

from .models import History, UserProfile, Transaction, Paytm_history, GoldGame, SilverGame, DiamondGame, OtherGame, withdraw_requests, Carousal, Contact, RedEnvelope, Carousal1, Carousal2, Carousal3, Notifications, Home_description, Payu

# class AddressAdmin(admin.ModelAdmin):
#     list_display = [
#         'user',
#         'street_address',
#         'apartment_address',
#         'country',
#         'zip',
#         'address_type',
#         'default'
#     ]
#     list_filter = ['default', 'address_type', 'country']
#     search_fields = ['user', 'street_address', 'apartment_address', 'zip']

class PHAdmin(admin.ModelAdmin):
    list_filter = ['STATUS']
    search_fields = ['user']
    
class WDAdmin(admin.ModelAdmin):
    search_fields = ['paid']

class Historyadmin(admin.ModelAdmin):
    search_fields = ['user__username']    

class UserProfileAdmin(admin.ModelAdmin):
    search_fields = ['user__username']     


admin.site.register(withdraw_requests,WDAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Transaction)
admin.site.register(History,Historyadmin)
admin.site.register(GoldGame)
admin.site.register(SilverGame)
admin.site.register(DiamondGame)
admin.site.register(OtherGame)
admin.site.register(Paytm_history)
admin.site.register(Carousal)
admin.site.register(Carousal1)
admin.site.register(Carousal2)
admin.site.register(Carousal3)
# admin.site.register(Sizes_class)
admin.site.register(Notifications)
admin.site.register(Home_description)
admin.site.register(RedEnvelope)
admin.site.register(Payu) 
admin.site.register(Contact)
