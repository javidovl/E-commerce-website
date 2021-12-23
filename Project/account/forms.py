from collections import namedtuple
from django import forms
from django.contrib.auth import get_user_model
from django.db.models.expressions import Exists
from django.utils.translation import ugettext_lazy as _
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.forms import ModelForm
from .models import BillingAddress
# from passwords.fields import PasswordField

Usermodel=get_user_model()


class Login_Form(forms.Form):
    login_email=forms.EmailField()
    login_password = forms.CharField(widget=forms.PasswordInput())

class Register(forms.Form):
    register_name=forms.CharField(max_length=255)
    register_email=forms.EmailField()
    register_phone_number=forms.CharField(max_length=255)
    register_password = forms.CharField(widget=forms.PasswordInput())
    register_password_again = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cd = self.cleaned_data
        if cd.get('register_password') != cd.get('register_password_again'):
            self.add_error('register_password_again', "Passwords do not match!")
        if Usermodel.objects.filter(email=cd.get('register_email')).exists():
            self.add_error('register_email','The account with the email you indicated already exists!')
        return cd


        
    
    # def send_activation_email(self):
    #     cd = self.cleaned_data
    #     user = Usermodel.objects.get(email=cd.get('register_email'))
    #     email = EmailMessage('Subject', 'Body', to=[user])
    #     email.send()
    def save_user(self, request):
        cd = self.cleaned_data
        user = Usermodel(
            name=cd.get('register_name'),
            email=cd.get('register_email'),
            phone_number=cd.get('register_phone_number'),
            is_staff=False,
            is_superuser=False,
            is_active=False,
        )
        user.set_password(cd.get('register_password'))
        user.save()
        current_site = get_current_site(request)
        mail_subject = 'Activate your Sellshop account.'
        message = render_to_string('acc_active_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':account_activation_token.make_token(user),
        })
        to_email = self.cleaned_data.get('register_email')
        email = EmailMessage(
                    mail_subject, message, to=[to_email]
        )
        email.send()
        



class BillingAdressForm(ModelForm):
    class Meta:
        model = BillingAddress
        fields = "__all__"

    def set_user(self, request):
        self.billing_address_user = request.user