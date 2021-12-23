from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import RequestContext, Template
from checkout.models import Basket
from rest_framework.authtoken.models import Token



def basket(request):
    if request.user.is_authenticated:
        if Basket.objects.filter(user=request.user, is_order_placed=False).exists():
            return {'basket':Basket.objects.filter(user=request.user, is_order_placed=False).first()}

        else:
            Basket.objects.create(user=request.user, is_order_placed=False)
    else:
        return {'basket':None}
