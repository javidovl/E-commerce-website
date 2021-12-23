"""Sellshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.urls.conf import include
from blog.views import *
from product.views import *
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from core.views import *
from account.views import *
from product.views import *
from checkout.views import *
from api.views import *
from django.conf.urls.i18n import i18n_patterns
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('order-complete/<int:pk>/', OrderCompleteView.as_view(), name="order-complete"),
    path('login/', Login_View.as_view(), name='login'),
    path('product/<int:id>/', SingleProductView.as_view(), name="product"),
    path('products/', ProductListView.as_view(), name="product-list"),
    path('blog/<int:pk>/', SingleBlogView.as_view(), name="blog"),
    path('blogs/', Blog_View.as_view(), name="blogs"),
    path('about/', AboutView.as_view(), name="about"),
    path('card/', CardView.as_view(), name="cart"),
    path('checkout/', CheckoutView.as_view(), name="checkout"),
    path('contact/', ContactView.as_view(), name="contact"),
    path('404/', View_404.as_view(),name="error-404"),
    path('home/', HomeView.as_view(), name="index"),
    path('wishlist/', WishlistView.as_view(), name="wishlist"),
    path('my-account/', MyAccountView.as_view(), name="my-account"),
    path('api/',include('api.urls')),
    path('logout/', CustomLogoutView.as_view(), name="logout"),
    path('new_user_post/', NewUserRegister.as_view(), name="new_user_post"),
    path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        activate, name='activate'),
    

    #Password Reset
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
