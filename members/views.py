from django.shortcuts import render, redirect
from django.views.generic import CreateView, TemplateView, DetailView, FormView
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistrationForm, PasswordForgotForm
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from myapp.models import Order
from .forms import PasswordForgotForm, PasswordResetForm
from django.contrib.auth.models import User
from .utils import password_reset_token
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
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


class PasswordForgotView(FormView):
    template_name = "registration/passwordforgot.html"
    form_class = PasswordForgotForm
    success_url = '/members/passwordforgot?msg=sent'

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        url = self.request.META['HTTP_HOST']
        user = User.objects.get(email=email)
        user = user
        text_content = 'Please Click the link below to reset your password.'
        html_content = url + "/members/password-reset/" + email + \
            "/" + password_reset_token.make_token(user) + "/"
        send_mail(
            'Password Reset Link | Django Ecommerce',
            text_content + html_content,
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )


        return super().form_valid(form)


class PasswordResetView(FormView):
    template_name = "registration/passwordreset.html"
    form_class = PasswordResetForm
    success_url = "/members/login"

    def dispatch(self, request, *args, **kwargs):
        email = self.kwargs.get("email")
        user = User.objects.get(email=email)
        token = self.kwargs.get("token")
        if user is not None and password_reset_token.check_token(user, token):
            pass
        else:
            return redirect(reverse("passworforgot") + "?msg=error")

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        password = form.cleaned_data['new_password']
        email = self.kwargs.get("email")
        user = User.objects.get(email=email)
        user.set_password(password)
        user.save()
        return super().form_valid(form)





    
    




