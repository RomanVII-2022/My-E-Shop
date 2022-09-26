from django.shortcuts import render, redirect
from .models import Category, Product, Cart, CartProduct
from django.http.response import JsonResponse
from django.views.generic import TemplateView, View, CreateView, FormView
from .forms import CheckoutForm
from django.urls import reverse_lazy
from django.db.models import Q
from django.core.paginator import Paginator


# Create your views here.
class EcoMixin(object):
    def dispatch(self, request, *args, **kwargs):
        cart_id = request.session.get('cart_id', None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            if request.user.is_authenticated and request.user:
                cart_obj.user = request.user
                cart_obj.save()
        return super().dispatch(request, *args, **kwargs)
    


def home(request):
    #products = Product.objects.all()
    p = Paginator(Product.objects.all(), 2)
    page = request.GET.get('page')
    products = p.get_page(page)
    return render(request, 'home.html', {'products':products})


def collectionsview(request):
    categories = Category.objects.filter(status=0)
    return render(request, 'collections.html', {'categories':categories})


def categoryitemsview(request, category_name):
    category = Category.objects.get(name=category_name)
    products = Product.objects.filter(category=category)
    return render(request, 'categoryitems.html', {'products':products, 'category':category})


def productdetailview(request, product_id):
    product = Product.objects.get(pk=product_id)
    return render(request, 'productdetail.html', {'product':product})


class AddCartView(EcoMixin, TemplateView):
    template_name = "addtocart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_id = self.kwargs['prod_id']
        product_obj = Product.objects.get(id=product_id)

        cart_id = self.request.session.get('cart_id', None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            product_in_cart = cart_obj.cartproduct_set.filter(product=product_obj)
            if product_in_cart.exists():
                cartproduct = product_in_cart.last()
                cartproduct.quantity += 1
                cartproduct.subtotal += product_obj.selling_price
                cartproduct.save() 
                cart_obj.total += product_obj.selling_price
                cart_obj.save()
            else:
                cartproduct = CartProduct.objects.create(cart=cart_obj, product=product_obj, quantity=1, subtotal=product_obj.selling_price) 
                cart_obj.total += product_obj.selling_price
                cart_obj.save()
        else:
            cart_obj = Cart.objects.create(total=0)
            self.request.session['cart_id'] = cart_obj.id
            cartproduct = CartProduct.objects.create(cart=cart_obj, product=product_obj, quantity=1, subtotal=product_obj.selling_price) 
            cart_obj.total += product_obj.selling_price
            cart_obj.save()

        return context


class MyCartView(EcoMixin, TemplateView):
    template_name = "mycart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get('cart_id', None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
        else:
            cart = None
        context['cart'] = cart

        return context


class CartManageView(EcoMixin, View):
    def get(self, request, *args, **kwargs):
        cart_id = self.kwargs['cart_id']
        action = request.GET.get('action')
        cart_obj = CartProduct.objects.get(id=cart_id)
        cart = Cart.objects.get(id=cart_obj.cart.id)
        if action == "inc":
            cart_obj.quantity += 1
            cart_obj.subtotal += cart_obj.product.selling_price
            cart_obj.save()
            cart.total += cart_obj.product.selling_price
            cart.save()
        elif action == "dec":
            cart_obj.quantity -= 1
            cart_obj.subtotal -= cart_obj.product.selling_price
            cart_obj.save()
            if cart_obj.quantity == 0:
                cart_obj.delete()            
            cart.total -= cart_obj.product.selling_price
            cart.save()
        elif action == "rmv":
            cart.total -= cart_obj.subtotal
            cart.save()
            cart_obj.delete()
        
        return redirect('mycart')


class EmptyCartView(EcoMixin, View):
    def get(self, request, *args, **kwargs):
        cart_id = request.session.get('cart_id', None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            cart_obj.cartproduct_set.all().delete()
            cart_obj.total = 0
            cart_obj.save()
        return redirect('mycart')


class CheckoutView(EcoMixin, CreateView):
    template_name = "checkout.html"
    form_class = CheckoutForm
    success_url = reverse_lazy('checkout')


    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user:
            pass
        else:
            return redirect('/members/login?next=/checkout')


        return super().dispatch(request, *args, **kwargs)
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get('cart_id', None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            context["cart_obj"] = cart_obj
        else:
            cart_obj = None

        return context

    def form_valid(self, form):
        cart_id = self.request.session.get('cart_id', None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            form.instance.cart = cart_obj
            form.instance.subtotal = cart_obj.total
            form.instance.discount = 0
            form.instance.total = cart_obj.total
            form.instance.order_status = "Order Received"
            del self.request.session['cart_id']

        else:
            return redirect('home')
        return super().form_valid(form)


class SearchView(TemplateView):
    template_name = "search.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.method == "GET":
            name = self.request.GET['search']
            products = Product.objects.filter(Q(name__contains=name) | Q(description__contains=name))
        context["products"] = products
        return context
    


        
    
    
    
