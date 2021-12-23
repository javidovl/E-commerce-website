from django.http.response import Http404, HttpResponseRedirect
from Sellshop.baseview import BaseTemplateView
from account.models import User
from django.shortcuts import render
from django.views.generic import TemplateView, DetailView
from blog.models import Blog, Review_Blog, BlogCategory
from django.views.generic import TemplateView


from .forms import ReviewBlogForm
from itertools import chain
from product.models import Category
# Create your views here.

class Blog_View(BaseTemplateView):
    template_name = 'blog.html'
    def get(self, request, *args, **kwargs):
        context={'blogs':Blog.objects.all()}
        return render(request, self.template_name, context)
        

class SingleBlogView(DetailView):
    template_name='single-blog.html'
    http_method_names = ['get', 'post']
    model=Blog
    context_object_name="chosen_blog"


    def get_context_data(self,*args, **kwargs):
        context= super().get_context_data(**kwargs)
        form=ReviewBlogForm()
        last_3_blog=Blog.objects.all().order_by('-created_at').exclude(id=self.kwargs['pk'])[:3]
        context['last_3_blog']=last_3_blog
        context['form']=form
        context['parent_categories']=BlogCategory.objects.filter(parent_category=None)
        context['related_blogs']=self.get_related_blogs()
        return context

    def get_related_blogs(self):
        blog=self.get_object()
        category = blog.category
        related_blogs = Blog.objects.filter(category=blog.category).exclude(id=blog.id)
        if related_blogs.count() < 3:
            categories = [category.id]
            while category.parent_category:
                category = category.parent_category
                categories.append(category.id)
            related_blogs = Blog.objects.filter(category__id__in=categories).exclude(id=blog.id).order_by('-id')[:3]
        return related_blogs                

    def post(self,request, *args, **kwargs):
        form=ReviewBlogForm(request.POST)

        if form.is_valid():
            cd=form.cleaned_data
            name=cd['name']
            email=cd['email']
            comment=cd['comment']
            review=Review_Blog(reviewer_name=name, reviewer_email=email, review_text=comment, blog=Blog.objects.filter(id=self.kwargs['pk']).first(), parent=None)

            review.save()
        
        return HttpResponseRedirect(f"/blog/{self.kwargs['pk']}")

   