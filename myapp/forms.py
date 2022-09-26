from django import forms
from .models import Order
from django.contrib.auth.models import User


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('ordered_by', 'shipping_address', 'mobile', 'email')


class PasswordForgotForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'
