from django.core.validators import MinLengthValidator
from django.db import models
from django.db.models import Avg
from django.db.models.deletion import CASCADE
from django.utils import tree


# Create your models here.

from django.db import models

class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)
    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value':self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)


class Category(models.Model):
    category_title=models.CharField(max_length=255)
    parent_category=models.ForeignKey('self', on_delete=models.SET_NULL, related_name="child", null=True, blank=True)

    def __str__(self):
        return self.category_title

class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.CharField(max_length=100)
    category=models.ForeignKey(Category, on_delete=models.CASCADE, related_name="categories")
    description=models.TextField()
    
    @property
    def category_name(self):
        return self.category.category_title

    @property
    def sizes_in_stock(self):
        minified=self.versions.all().values_list('size', flat=True).distinct()
        return minified
    
    @property
    def colors_of_product(self):
        minified=self.versions.all().values_list('color', flat=True).distinct()
        return minified



    def __str__(self):
        return self.name 

class ProductVersion(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE, related_name='versions')
    colors=(

        ("dodgerblue3", "dodgerblue3"),
        ("hexcyan", "hexcyan"),
        ("tomato", "tomato"),
        ("pumpkin", "pumpkin"),
        ("darksalmon","darksalmon"),
        ("deepbluesky", "deepbluesky"),
        ("lightsalmon","lightsalmon")



    )
    color=models.CharField(choices=colors, max_length=255)
    stock_quantity=models.IntegerField()
    is_main=models.BooleanField()
    sizes=(

        ("xs", "xs"),
        ("s","s"),
        ("m","m"),
        ("l", "l"),
        ("xl","xl",),
        
    )
    size=models.CharField(choices=sizes, max_length=255)

    def __str__(self):
        return f"{self.product.name}-{self.color}-{self.size}"

    @property
    def in_stock(self):
        return self.stock_quantity > 0

    @property
    def price(self):
        return self.product.price
    
    @property
    def name(self):
        return self.product.name
    
    @property
    def description(self):
        return self.product.description
    
    @property
    def category(self):
        return self.product.category.id
    
    @property
    def category_name(self):
        return self.product.category.category_title
    
    @property
    def sizes_in_stock(self):
        minified=self.product.versions.all().values_list('size', flat=True).distinct()
        return minified
    
    @property
    def colors_of_product(self):
        minified=self.product.versions.all().values_list('color', flat=True).distinct()
        return minified

    @property
    def image_url(self):
        return self.images_of_pv.filter(is_main=True).first().image.url

    @property
    def review_count(self):
        return self.product.reviews_of_product.count()
    

class Review_Product(models.Model):
    reviewer_name = models.CharField(max_length=50)
    reviewer_email = models.EmailField()
    review_text=models.TextField()
    review_star=IntegerRangeField(min_value=1, max_value=5, null=True, blank=True)
    product_id=models.ForeignKey(Product, related_name="reviews_of_product", on_delete=CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.reviewer_name






