from django.contrib import admin

# from .models import Item, OrderItem, Order, Payment, Coupon, Refund, Address, UserProfile, Transaction, TravelDetails, Paytm_history, Paytm_order_history, ClubJoin, Carousal, Sizes_class, Reviews, Team, Ads, Itemimage, Itemdealer, Myorder, Sales, Categories, Extrasales, CarousalClub, ReviewsImage, Contact, FAQs

from .models import History, UserProfile, Transaction, Paytm_history, GoldGame, SilverGame, DiamondGame, OtherGame, withdraw_requests, Carousal, Contact, RedEnvelope, Carousal1, Carousal2, Carousal3

# def make_refund_accepted(modeladmin, request, queryset):
#     queryset.update(refund_requested=False, refund_granted=True)


# make_refund_accepted.short_description = 'Update orders to refund granted'


# class OrderAdmin(admin.ModelAdmin):
#     list_display = ['user',
#                     'ordered',
#                     'being_delivered',
#                     'received',
#                     'refund_requested',
#                     'refund_granted',
#                     'shipping_address',
#                     'billing_address',
#                     'payment',
#                     'coupon'
#                     ]
#     list_display_links = [
#         'user',
#         'shipping_address',
#         'billing_address',
#         'payment',
#         'coupon'
#     ]
#     list_filter = ['ordered',
#                    'being_delivered',
#                    'received',
#                    'refund_requested',
#                    'refund_granted']
#     search_fields = [
#         'user__username',
#         'ref_code'
#     ]
#     actions = [make_refund_accepted]


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

# class ItemAdmin(admin.ModelAdmin):
#     search_fields = ['title', 'pincode', 'slug', 'tag', 'category']

# class ClubAdmin(admin.ModelAdmin):
#     search_fields = ['user__username']
#     list_filter = ['premium', 'desig', 'fund_transfered']
    
# class ItemimageAdmin(admin.ModelAdmin):
#     search_fields = ['item__title']
    
# class ItemdealerAdmin(admin.ModelAdmin):
#     search_fields = ['item__title']
    
# class MyordersAdmin(admin.ModelAdmin):
#     search_fields = ['user__username', 'item__title']

# class CategoriesAdmin(admin.ModelAdmin):
#     search_fields = ['name']
    
# class SalesAdmin(admin.ModelAdmin):
#     search_fields = ['sale_name', 'item__title']

class Historyadmin(admin.ModelAdmin):
    search_fields = ['user__username']    

class UserProfileAdmin(admin.ModelAdmin):
    search_fields = ['user__username']    


admin.site.register(withdraw_requests)
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
# admin.site.register(Reviews)
# admin.site.register(ReviewsImage)
admin.site.register(RedEnvelope)
# admin.site.register(FAQs)
admin.site.register(Contact)
