"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from . import views
from .views import AddCartView, MyCartView, CartManageView, EmptyCartView, CheckoutView, SearchView

urlpatterns = [
    path('', views.home, name="home"),
    path('collections', views.collectionsview, name="collections"),
    path('categoryitems/<category_name>', views.categoryitemsview, name="categoryitems"),
    path('productdetail/<product_id>', views.productdetailview, name="productdetail"),
    path("add-to-cart/<int:prod_id>", AddCartView.as_view(), name="addtocart"),
    path('my-cart', MyCartView.as_view(), name="mycart"),
    path('managecart/<int:cart_id>', CartManageView.as_view(), name='managecart'),
    path('emptycart', EmptyCartView.as_view(), name="emptycart"),
    path('checkout', CheckoutView.as_view(), name='checkout'),
    path('search', SearchView.as_view(), name='search'),
]

