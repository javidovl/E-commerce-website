from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect
from core.forms import ContactsForm, SubscribeForm


def subscribe(request):
    form=SubscribeForm()
    return {'subscribe_form':form}

def contact(request):
    form =ContactsForm()
    return {'contacts_form':form}
