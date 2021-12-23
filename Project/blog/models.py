from django.db import models
from account.models import User
import datetime
from django.utils.timezone import now
from django.urls import reverse_lazy


class BlogCategory(models.Model):
    title=models.CharField(max_length=255)
    parent_category=models.ForeignKey('self', on_delete=models.SET_NULL, related_name="child", null=True, blank=True)

    def __str__(self):
        return self.title

class Blog(models.Model):
    blog_title=models.CharField(max_length=255)
    blog_writer=models.ForeignKey(User, on_delete=models.CASCADE, related_name='blogs')
    blog_content=models.TextField(default=None)
    category=models.ForeignKey(BlogCategory, on_delete=models.CASCADE, related_name="blogs")
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.blog_title



class Review_Blog(models.Model):
    reviewer_name = models.CharField(max_length=50)
    reviewer_email = models.EmailField()
    review_text=models.TextField()
    blog=models.ForeignKey(Blog, related_name="reviews", on_delete=models.CASCADE)
    parent=models.ForeignKey('self', on_delete=models.SET_NULL, related_name="child", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return self.reviewer_name


class BlogImage(models.Model):
    blog=models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="images_of_blog")
    image_370x255=models.ImageField()
    image_870x400=models.ImageField()

    