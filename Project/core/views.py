from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.generic import FormView
from django.views.generic.base import TemplateView
from rest_framework.views import APIView
from django.views import View

from product.models import Product
from .forms import SubscribeForm, ContactsForm
from django.urls import resolve
from Sellshop.baseview import BaseTemplateView
from blog.models import *
# Create your views here.

# class AllPagesHandler():

#     def post_of_forms(self, request):
#         if request.method=='POST':
#             if 'subscribe_form' in request.POST:
#                 sub_form=SubscribeForm(request.POST)
#                 if sub_form.is_valid():
#                     sub_form.save()
#             elif 'contact_form' in request.POST:
#                 contact_form=ContactsForm(request.POST)
#                 if contact_form.is_valid():
#                     contact_form.save()


class AboutView(BaseTemplateView):
    template_name="about.html"



class ContactView(BaseTemplateView):
    template_name="contact.html"

    
    
class View_404(BaseTemplateView):
    template_name='error-404.html'


class HomeView(BaseTemplateView):
    template_name='index.html'

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['last_blogs_3']=Blog.objects.all().order_by('-created_at')[:3]
        context['last_blogs_6']=Blog.objects.all().order_by('-created_at')[3:9]
        context['products']=Product.objects.all()[:3]
        return context



        
