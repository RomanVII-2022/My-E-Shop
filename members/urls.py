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
from .views import RegistrationView, LoginView, ProfileView, OrderDetailView, PasswordForgotView, PasswordResetView

urlpatterns = [
    path('registar', RegistrationView.as_view(), name="registar"),
    path('login', LoginView.as_view(), name='login'),
    path('profile', ProfileView.as_view(), name="profile"),
    path('orderdetail/<int:pk>', OrderDetailView.as_view(), name='orderdetail'),
    path('passwordforgot', PasswordForgotView.as_view(), name="passwordforgot"),
    path('password-reset/<email>/<token>/', PasswordResetView.as_view(), name="passwordreset"),
]

