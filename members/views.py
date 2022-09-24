from django.shortcuts import render, redirect
from django.views.generic import CreateView, TemplateView, DetailView
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistrationForm
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from myapp.models import Order

# Create your views here.
class RegistrationView(SuccessMessageMixin, CreateView):
    form_class = RegistrationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy('login')
    success_message = "You were registered successfully"


    def get_success_url(self):
        if "next" in self.request.GET:
            next_url = self.request.GET.get('next')
            return next_url
        else:
            return self.success_url


class LoginView(LoginView):
    template_name = "registration/login.html"
    form_class = AuthenticationForm
    success_url = reverse_lazy('home')


    def get_success_url(self):
        if "next" in self.request.GET:
            next_url = self.request.GET.get('next')
            return next_url
        elif "back" in self.request.GET:
            back_url = self.request.GET.get('back')
            return back_url
        else:
            return self.success_url



class ProfileView(TemplateView):
    template_name = "profile.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user:
            pass
        else:
            return redirect('login?back=/members/profile')
        return super().dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["user"] = user
        orders = Order.objects.filter(cart__user=user)
        context['orders'] = orders
        return context


class OrderDetailView(DetailView):
    template_name = "orderdetail.html"
    model = Order

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user:
            order_id = self.kwargs['pk']
            order_obj = Order.objects.get(id=order_id)
            if request.user != order_obj.cart.user:
                return redirect('profile')
        else:
            return redirect('login?back=/members/profile')
        return super().dispatch(request, *args, **kwargs)


    
    




