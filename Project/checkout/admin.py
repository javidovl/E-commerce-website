from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Basket)
admin.site.register(BasketItem)
admin.site.register(Wishlist)
admin.site.register(Order)