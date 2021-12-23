from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from product.views import ProductListView
from .views import *
from rest_framework_simplejwt import views as jwt_views
from rest_framework.authtoken import views


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('products/', ProductListApiView.as_view()),
    path('category/', CategoryListApiView.as_view()),
    path('category/create/', CreateCategoryApiView.as_view()),
    path('category/delete/<int:pk>/', DeleteCategoryApiView.as_view()),
    path('category/update/<int:pk>/', UpdateCategoryApiView.as_view()),
    path('products/delete/<int:pk>/', DeleteProductApiView.as_view()),
    path('products/update/<int:pk>/', UpdateProductApiView.as_view()),
    path('products/create/', CreateProductApiView.as_view()),
    path('products/get_single/<int:pk>/', GetSingleProductApiView().as_view()),
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    # path('token/', views.obtain_auth_token),
    path('basket/', BasketApiView.as_view(), name='basket_api'),
    path('basket/delete_item/',BasketItemDeleteApiView().as_view(), name='basket_item_delete_api'),
    path('accounts/create', UserCreateApiView.as_view(), name='create_user_api'),
    path('comments/create', CommentCreateApiView.as_view(), name='create_comment_api'),
    path('wishlist/', WishlistApiView.as_view(), name='wishlist_api'),
    path('product_version/', ProductVersionApiView.as_view(), name='product_version_api'),
    path('order/', OrderApiView.as_view(), name='order_api'),
]