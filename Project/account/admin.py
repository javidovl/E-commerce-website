from django.contrib import admin
from .models import *



# Registering custom one.
admin.site.register(User)
admin.site.register(BillingAddress)