from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views import View
from Sellshop.baseview import BaseTemplateView
from checkout.models import Basket, Wishlist
from django.contrib.auth.mixins import LoginRequiredMixin
from checkout.models import Order
# Create your views here.



class CheckoutView(BaseTemplateView):
    template_name='checkout.html'



class CardView(LoginRequiredMixin, BaseTemplateView):
    template_name='cart.html'
    login_url = '/login'
    redirect_field_name = login_url


class WishlistView(LoginRequiredMixin, BaseTemplateView):
    template_name='wishlist.html'
    login_url = '/login'
    redirect_field_name = login_url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['wishlist'] = Wishlist.objects.get_or_create(user=self.request.user)[0]
        return context

class OrderCompleteView(BaseTemplateView):
    template_name='order-complete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = Order.objects.filter(id=self.kwargs['pk']).first()
        return context



