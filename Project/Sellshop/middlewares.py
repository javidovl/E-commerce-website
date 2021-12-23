from django.http.response import HttpResponseRedirect
from core.forms import SubscribeForm, ContactsForm

class CustomFormHandlerMW:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if 'subscribe_form' in request.POST:
            sub_form=SubscribeForm(request.POST)
            if sub_form.is_valid():
                sub_form.save()
        elif 'contact_form' in request.POST:
            contact_form=ContactsForm(request.POST)
            if contact_form.is_valid():
                contact_form.save()

        response = self.get_response(request)
        return response


