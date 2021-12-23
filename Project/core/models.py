from django.db import models
from django.utils.crypto import get_random_string

from product.models import ProductVersion

# Create your models here.
class Subscriber(models.Model):
    email=models.EmailField()

    def __str__(self):
        return self.email

class Contact(models.Model):
    name=models.CharField(max_length=255)
    email=models.EmailField()
    message=models.TextField()
    def __str__(self):
        return self.name


class Photo(models.Model):
    product_version=models.ForeignKey(ProductVersion, on_delete=models.CASCADE, related_name='images_of_pv')
    image=models.ImageField()
    is_main=models.BooleanField(default=False)
    
    def __str__(self):
        return self.image.url