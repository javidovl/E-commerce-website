from django import forms
from django.forms import fields
from .models import Review_Blog

class ReviewBlogForm(forms.Form):
    name=forms.CharField(max_length=255)
    email=forms.EmailField()
    comment = forms.CharField(widget=forms.Textarea)


# class ReviewBlogFormTest(forms.ModelForm):
#     class Meta():
#         model=Review_Blog
#         fields=['reviewer_name','reviewer_email','review_text','blog']
    
