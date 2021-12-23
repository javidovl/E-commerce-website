import math
from typing import ContextManager
from django.shortcuts import render
from blog.models import BlogCategory
from checkout.models import Basket, BasketItem
from .models import Category, Product, ProductVersion, Review_Product
from django.views.generic import ListView
from django.core.paginator import Paginator
from rest_framework.generics import ListAPIView
from django.db.models import Avg
from django.http import HttpResponseRedirect
from Sellshop.baseview import BaseTemplateView
from .forms import Review_Product_Form
# Create your views here.


from django.views.generic import TemplateView

class ProductListView(ListView):
    template_name='product-list.html'
    paginate_by=3
    model=ProductVersion
    context_object_name = "products"
    queryset=ProductVersion.objects.distinct('product')
        

    def get_page_contexts(self):
        page_number = int(self.request.GET.get('page',1))
        qs=self.get_queryset()
        last_digit=self.paginate_by*page_number
        first_digit=last_digit-self.paginate_by+1

        if page_number*self.paginate_by>qs.count():
            last_digit=qs.count()
        return first_digit, last_digit
    
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        first_digit, last_digit=self.get_page_contexts()
        context['first_digit']=first_digit
        context['last_digit']=last_digit
        context['products_qs_count']=ProductVersion.objects.all().count()
        context['parent_categories']=Category.objects.filter(parent_category=None)
        return context

    def post(self, request, *args, **kwargs):
        return HttpResponseRedirect(request.path_info)

class SingleProductView(BaseTemplateView):
    template_name="single-product.html"
    

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['review_form']=Review_Product_Form()
        context['chosen_product']=Product.objects.filter(id=self.kwargs['id']).first()
        avg_star=context['chosen_product'].reviews_of_product.all().aggregate(Avg('review_star'))['review_star__avg']
        context['related_products']=self.get_related_products(context['chosen_product'])
        context['main_pv']=ProductVersion.objects.filter(product=context['chosen_product'], is_main=True).first()       
        if avg_star:
            context['average_of_reviews']="{:.2f}".format(avg_star)
        else:
            context['average_of_reviews']=0

        return context

    def get_related_products(self, product):
        category = product.category
        related_blogs = Product.objects.filter(category=product.category).exclude(id=product.id)
        if related_blogs.count() < 5:
            categories = [category.id]
            while category.parent_category:
                category = category.parent_category
                categories.append(category.id)
            related_blogs = Product.objects.filter(category__id__in=categories).exclude(id=product.id).order_by('-id')[:3]
        return related_blogs      

    