from re import template
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponse
from django.views.generic.base import TemplateView, View
from Sellshop.baseview import BaseTemplateView
from account.forms import Login_Form, Register
from django.shortcuts import render
from django.contrib.auth.views import LogoutView
from rest_framework.serializers import *
from .models import BillingAddress
from .forms import BillingAdressForm
from .forms import Register
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.core.mail import EmailMessage
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
# Create your views here.
Usermodel=get_user_model()

class Login_View(BaseTemplateView):
    template_name = 'login.html'

    def get(self, request):
        context={'login_form':Login_Form(), 'register_form':Register()}
        return render(request, self.template_name, context)

    def post(self, request,  *args, **kwargs):
            login_form=Login_Form(request.POST)
            if login_form.is_valid():
                user=authenticate(email=login_form.cleaned_data['login_email'], password=login_form.cleaned_data['login_password'])
                if user is not None:
                    login(request, user)
                    return HttpResponseRedirect('/home')
                else:
                    login_form=Login_Form()
                    register_form=Register()

                return render(request, self.template_name, {'login_form':login_form, 'register_form':register_form})
            else:
                return HttpResponseRedirect('/login')




class NewUserRegister(View):
    template_name = 'login.html'
    def post(self, request):
        form = Register(request.POST)
        if form.is_valid():
            form.save_user(request)          
            return HttpResponseRedirect('/login')
        else:
            return render(request, self.template_name, {'register_form': form})


class MyAccountView(LoginRequiredMixin, BaseTemplateView):
    template_name='my-account.html'
    login_url = '/login'
    redirect_field_name = login_url

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['billing_form']=BillingAdressForm()
        context['billing_address']=BillingAddress.objects.filter(billing_address_user=self.request.user)
        return context

    def post(self, request):
        form = BillingAdressForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/my-account')
        else:
            return render(request, self.template_name, {'billing_form': form})

class CustomLogoutView(LogoutView):
    next_page='/home'

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Usermodel.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


# class CustomPasswordResetView(PasswordResetView):
#     email_template_name = 'my-account.html'
#     form_class = PwdResetForm
#     template_name = 'password/password_reset_form.html'
#     success_url="password_reset_email_confirm/"
# class CustomPasswordResetConfirmView(PasswordResetConfirmView):
#     template_name   = "password/password-reset-confirm.html"
#     # success_url     = "password_reset_complete/"
#     success_url     = '/'
#     form_class      =  PwdResetConfirmForm
# class CustomResetEmailConfirmView(TemplateView):
#     template_name   = "password/reset_status.html"
# class CustomPasswordResetCompleteView(TemplateView):
#     template_name   = "password/reset_status.html"