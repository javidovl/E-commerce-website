from django.http.response import HttpResponseRedirect
from django.views.generic import TemplateView

class BaseTemplateView(TemplateView):
    
    def post(self, request, *args, **kwargs):
        return HttpResponseRedirect(request.path_info)