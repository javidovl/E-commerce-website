from django.contrib.sites.requests import RequestSite
from django.http.response import HttpResponse, HttpResponseRedirect
from rest_framework.views import APIView
from account.models import User
from product.models import *
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView
from .serializers import CategorySerializer, ProductSerializer
from .serializers import *
from rest_framework.permissions import IsAuthenticated, AllowAny
# Create your views here.


from django.views.generic import TemplateView

class ProductListApiView(ListAPIView):
    model=Product
    serializer_class=ProductSerializer
    queryset=Product.objects.all()

     
    def get_queryset(self):
        qs= super().get_queryset()
        if self.request.query_params.get('category'):
            qs=qs.filter(category__in=self.get_subcategories_of_parent(self.get_category_id()))
        if self.request.query_params.get('min_price') and self.request.query_params.get('max_price'):
            for product in qs:
                if float(product.price)<float(self.request.query_params.get('min_price')) or float(product.price)>float(self.request.query_params.get('max_price')):
                    qs=qs.exclude(id=product.id)
        if self.request.query_params.get('size'):
            for product in Product.objects.all():
                serializer=ProductSerializer(product)
                if self.request.GET.get('size') not in serializer.data['sizes_in_stock']:
                    qs=qs.exclude(id=product.id)
        if self.request.query_params.get('color'):
            for product in Product.objects.all():
                serializer=ProductSerializer(product)
                if self.request.GET.get('color').lower() not in serializer.data['colors_of_product']:
                    qs=qs.exclude(id=product.id)
        return qs

    def get_category_id(self):
        category_id=self.request.GET.get('category')
        return category_id

    def get_subcategories_of_parent(self, category_id):
        category_items=[category_id]
        for category_item in Category.objects.filter(parent_category=category_id).all():
            if not category_item.child.first():
                category_items.append(category_item)
            else:
                category_items.append(self.get_subcategories_of_parent(category_item.id))
        return category_items


class DeleteProductApiView(APIView):
    model=Product
    serializer_class=ProductSerializer
    queryset=Product.objects.all()

    def delete(self, request, pk):
        category=Category.objects.get(id=pk)
        category.delete()
        return Response("Category is deleted", status=status.HTTP_204_NO_CONTENT)
    
    def get(self, request, pk):
        category=Category.objects.get(id=pk)
        serializer=CategorySerializer(instance=category)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateProductApiView(UpdateAPIView):
    model=Product
    serializer_class=ProductSerializer
    queryset=Product.objects.all()

    def get(self, request, pk):
        product=Product.objects.get(id=pk)
        serializer=ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateProductApiView(CreateAPIView):
    model=Product
    serializer_class=ProductSerializer
    queryset=Product.objects.all()

    def get(self, request):
        product=Product.objects.all()
        serializer=ProductSerializer(product, many=True)
        return Response(serializer.data)


class GetSingleProductApiView(APIView):
    model=Product
    serializer_class=ProductSerializer
    queryset=Product.objects.all()

    def get(self, request, pk):
        product=Product.objects.get(id=pk)
        serializer=ProductSerializer(product)
        return Response(serializer.data)


class CategoryListApiView(ListAPIView):
    model=Category
    serializer_class=CategorySerializer
    queryset=Category.objects.all()


class CreateCategoryApiView(CreateAPIView):
    model=Category
    serializer_class=CategorySerializer
    queryset=Category.objects.all()

    def get(self, request):
        category=Category.objects.all()
        serializer=CategorySerializer(category, many=True)
        return Response(serializer.data)


class DeleteCategoryApiView(APIView):
    model=Category
    serializer_class=CategorySerializer
    queryset=Category.objects.all()

    def delete(self, request, pk):
        category=Category.objects.get(id=pk)
        category.delete()
        return Response("Category is deleted", status=status.HTTP_204_NO_CONTENT)
    
    def get(self, request, pk):
        category=Category.objects.get(id=pk)
        serializer=CategorySerializer(instance=category)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateCategoryApiView(UpdateAPIView):
    model=Category
    serializer_class=CategorySerializer
    queryset=Category.objects.all()

    def get(self, request, pk):
        category=Category.objects.get(id=pk)
        serializer=CategorySerializer(instance=category)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BasketApiView(APIView):
    serializer_class=BasketSerializer
    permission_classes=[IsAuthenticated]

    def get(self, request):
        serializer=self.serializer_class(request.user.basket_of_user.filter(is_order_placed=False), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
            product_version_id, quantity=self.get_data(request)
            basket = Basket.objects.filter(user=request.user, is_order_placed=False).first()
            if ProductVersion.objects.filter(id=product_version_id).exists():
                product_version=ProductVersion.objects.get(id=product_version_id)
            else:
                message={"message": "Product version does not exist"}
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
            if quantity>product_version.stock_quantity:
                    message={'message': f"There is no enough quantity of this product, there are only {product_version.stock_quantity} this type if items in stock!"}
                    return Response(message, status=status.HTTP_400_BAD_REQUEST)
            if BasketItem.objects.filter(basket=basket, product_version_id=product_version_id).exists():
                basket_item=BasketItem.objects.get(basket=basket, product_version_id=product_version_id)
                basket_item.quantity+=quantity
                basket_item.save()
            else:
                basket_item=BasketItem.objects.create(product_version=ProductVersion.objects.get(id=product_version_id), quantity=quantity, basket=basket)
            if basket_item:
                basket.product_list.add(basket_item)
                message={'succees':True, 'message':"Product is added to basket"}
                return Response(message, status=status.HTTP_201_CREATED)
            message={'succees':False, 'message':"Product is not added to basket"}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
    
    def get_data(self, request):
        product_version_id=request.data.get('product_version_id')
        quantity=int(request.data.get('quantity'))
        return product_version_id, quantity



class BasketItemDeleteApiView(APIView):

    serializer_class=BasketSerializer
    permission_classes=[IsAuthenticated]

    def delete(self,request):
        id=request.data.get('basket_item_id')
        basketItem=BasketItem.objects.get(id=id)
        if basketItem.basket_of_products.first().user==request.user:
            basketItem.delete()
            return Response("Basket item is deleted", status=status.HTTP_204_NO_CONTENT)
        return Response("Basket item is not deleted", status=status.HTTP_400_BAD_REQUEST)


class UserCreateApiView(APIView):
    serializer_class=UserCreateSerializer
    queryset=get_user_model().objects.all()
    permission_classes=[AllowAny]

    def post(self, request):
        serializer=self.serializer_class(data=request.data)
        if serializer.is_valid():
            user=serializer.save()
            user.set_password(serializer.validated_data['password'])
            user.save()
            message={'succees':True, 'message':"User is created"}
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            message={'succees':False, 'message':"User is not created"}
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    # from rest_framework.authtoken.models import Token
    # from django.conf import settings
    # token = Token.objects.create(user=settings.AUTH_USER_MODEL)
    # user_with_token = Token.objects.get(user=user)
    # is_tokened = Token.objects.filter(user=request.user).exist()  # Returns a boolean


class CommentCreateApiView(APIView):
    serializer_class=ProductReviewSerializer
    queryset=Review_Product.objects.all()
    permission_classes=[AllowAny]

    def post(self, request):
        serializer=self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WishlistApiView(APIView):
    serializer_class=WishlistSerializer
    queryset=Wishlist.objects.all()
    permission_classes=[IsAuthenticated]

    def post(self, request):
        product_version_id=request.data.get('product_version_id')
        print(product_version_id)   
        if request.user.wishlist_of_user.product_list.all().filter(id=product_version_id).exists():
            message={'succees':False, 'message':"Product is already in wishlist"}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        else:
            product_version=ProductVersion.objects.get(id=product_version_id)
            if product_version!=None:
                request.user.wishlist_of_user.product_list.add(product_version)
                message={'succees':True, 'message':"Product is added to wishlist", 'product_version_id':product_version_id}
                return Response(message, status=status.HTTP_201_CREATED)
            else:
                message={'succees':False, 'message':"Product is not added to wishlist"}
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request):
        product_version_id=request.data.get('product_version_id')
        if request.user.wishlist_of_user.product_list.all().filter(id=product_version_id).exists():
            product_version=ProductVersion.objects.get(id=product_version_id)
            request.user.wishlist_of_user.product_list.remove(product_version)
            message={'succees':True, 'message':"Product is removed from wishlist"}
            return Response(message, status=status.HTTP_204_NO_CONTENT)
        else:
            message={'succees':False, 'message':"Product is not in wishlist"}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)


class ProductVersionApiView(ListAPIView):
    serializer_class=ProductVersionSerializer
    queryset=ProductVersion.objects.all()
    permission_classes=[AllowAny]

    def get_queryset(self):
        qs= super().get_queryset()
        if self.request.query_params.get('category'):
            for pv in qs:
                if pv.product.category.id!=int(self.request.query_params.get('category')):
                    qs=qs.exclude(id=pv.id)
        if self.request.query_params.get('min_price') and self.request.query_params.get('max_price'):
            for product in qs:
                if float(product.price)<float(self.request.query_params.get('min_price')) or float(product.price)>float(self.request.query_params.get('max_price')):
                    qs=qs.exclude(id=product.id)
        if self.request.query_params.get('size'):
            for product_version in ProductVersion.objects.all():
                serializer=ProductVersionSerializer(product_version)
                if self.request.GET.get('size') != serializer.data['size']:
                    qs=qs.exclude(id=product_version.id)
        if self.request.query_params.get('color'):
           for product_version in ProductVersion.objects.all():
                serializer=ProductVersionSerializer(product_version)
                if self.request.GET.get('color').lower() != serializer.data['color']:
                    qs=qs.exclude(id=product_version.id)
        return qs


    def post(self, request):
        product_id=request.data.get('product_id')
        color=request.data.get('color')
        size=request.data.get('size').lower()
        if ProductVersion.objects.filter(product=product_id, color=color, size=size).exists():
            message={'succees':True, 'product_version_id':ProductVersion.objects.get(product=product_id, color=color, size=size).id}
            return Response(message, status=status.HTTP_201_CREATED)
        else:
            message={'succees':False, 'message':"Product version is not created"}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)


class OrderApiView(APIView):
    serializer_class=OrderSerializer
    queryset=Order.objects.all()
    permission_classes=[AllowAny]

    def post(self, request):
        user_id=request.data.get('user_id')
        billing_address_id=request.data.get('billing_address_id')
        basket_id=request.user.basket_of_user.filter(is_order_placed=False).first().id
        Order.objects.create(user=Usermodel.objects.get(id=user_id), billing_address=BillingAddress.objects.get(id=billing_address_id), basket=Basket.objects.get(id=basket_id))
        for basket_item in Basket.objects.get(id=basket_id).product_list.all():
            basket_item.product_version.stock_quantity-=basket_item.quantity
            basket_item.product_version.save()
        message={'succees':True, 'message':"Order is created", 'order_id':Order.objects.get(user=Usermodel.objects.get(id=user_id), billing_address=BillingAddress.objects.get(id=billing_address_id), basket=Basket.objects.get(id=basket_id, is_order_placed=False)).id}
        basket=Basket.objects.get(id=basket_id, is_order_placed=False)
        basket.is_order_placed=True
        basket.save()
        return Response(message, status=status.HTTP_201_CREATED)

        
        