from django.db import models
from django.contrib.auth import get_user_model
from account.models import BillingAddress
from product.models import Product, ProductVersion
import json
Usermodel=get_user_model()


class BasketItem(models.Model):
    product_version=models.ForeignKey(ProductVersion, on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    basket=models.ForeignKey('Basket', on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.product_version} - {self.quantity}"

    @property
    def price_of_basket_item(self):
        return float(self.product_version.product.price)*self.quantity
    



class Basket(models.Model):
    user=models.ForeignKey(Usermodel,on_delete=models.CASCADE, related_name="basket_of_user")
    product_list=models.ManyToManyField(BasketItem, related_name="basket_of_products", null=True, blank=True)
    is_order_placed=models.BooleanField(default=False)

    @property
    def product_features(self):
        result_dict={}
        for basket_item in self.product_list.all():
            specs=[]
            specs.append(basket_item.product_version.product.name)
            specs.append(basket_item.product_version.product.price)
            specs.append(basket_item.product_version.size)
            specs.append(basket_item.product_version.color)
            specs.append(basket_item.quantity)
            specs.append(basket_item.product_version.images_of_pv.all()[0].image.url)
            result_dict[str(basket_item.id)]=specs
        return result_dict
    
    @property
    def total_price(self):
        total=0
        for basket_item in self.product_list.all():
            total+=(float(basket_item.price_of_basket_item))
        return "{:.2f}".format(total)

    def __str__(self):
        return f"Basket of {self.user.email}"


class Wishlist(models.Model):
    user=models.OneToOneField(Usermodel,on_delete=models.CASCADE, related_name="wishlist_of_user", default=1)
    product_list=models.ManyToManyField(ProductVersion, related_name="wishlist_of_products", null=True, blank=True)



 
class Order(models.Model):
    user=models.ForeignKey(Usermodel, on_delete=models.CASCADE, related_name="order_of_user")
    billing_address=models.ForeignKey(BillingAddress, on_delete=models.CASCADE,)
    basket=models.ForeignKey(Basket, related_name="order_of_basket", on_delete=models.CASCADE )
    created_at=models.DateTimeField(auto_now_add=True)

    @property
    def total_price(self):
        total=0
        for basket_item in self.basket.product_list.all():
            total+=(float(basket_item.price_of_basket_item))
        return total