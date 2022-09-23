from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistrationForm
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin

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
        else:
            return self.success_url




