from django import forms
from django.forms import fields
from .models import Subscriber, Contact

class SubscribeForm(forms.ModelForm):

    class Meta():
        model=Subscriber
        fields="__all__"

    def save(self, commit=True):
        return super().save(commit=commit)

class ContactsForm(forms.ModelForm):

    class Meta():
        model=Contact
        fields="__all__"
