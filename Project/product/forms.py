from django.forms import ModelForm
from .models import Review_Product
class Review_Product_Form(ModelForm):
    class Meta:
        model=Review_Product
        fields=['reviewer_name', 'reviewer_email', 'review_text', 'review_star']            

