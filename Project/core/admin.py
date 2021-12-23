from django.contrib import admin

# Register your models here.

from product.models import Category, Product, Review_Product
from blog.models import Blog, Review_Blog
from account.models import *
from checkout.models import *
from .models import *


# class Category(admin.ModelAdmin):
#     pass
# class Blog(admin.ModelAdmin):
#     pass
# class Review_Product(admin.ModelAdmin):
#     pass
# class Review_Blog(admin.ModelAdmin):
#     pass
# class Contact(admin.ModelAdmin):
#     pass
# class Subscriber(admin.ModelAdmin):
#     pass



admin.site.register(Product)
admin.site.register(Blog)
admin.site.register(Review_Blog)
admin.site.register(Contact)
admin.site.register(Subscriber)
admin.site.register(Category)
admin.site.register(Photo)
admin.site.register(Review_Product)



