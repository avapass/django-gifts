from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout

from .models import Product
from .forms import CustomLoginForm

# Create your views here.

def hello(request):
    return render(request, "index.html")

def products_list(request):
    products = Product.objects.all()
    products = products.order_by("-price", "title")

    return render(request, "products.html", {"products": products})

def product(request, id):
    product = get_object_or_404(Product, id=id)
    is_favourite = False
    if product.favourite.filter(id=request.user.id).exists():
        is_favourite = True
    # try:
    #     product = Product.objects.get(id=id)
    # except Product.DoesNotExist:
    #     return HttpResponse("404")

    context = {
        'product': product,
        'is_favourite': is_favourite
    }
    return render(request, "product.html", context)

def favourite_list(request):
    user = request.user
    favourite_prod = user.favourite.all()
    return render(request, "favourite_list.html", {"favourite_prod": favourite_prod})

def favourite_prod(request, id):
    product = get_object_or_404(Product, id=id)
    if product.favourite.filter(id=request.user.id).exists():
        product.favourite.remove(request.user)
    else:
        product.favourite.add(request.user)
    return HttpResponseRedirect(product.get_absolute_url())

# def contact(request):
#     form = ContactForm()
#     if request.method == "POST":
#         form = ContactForm(request.POST)
#         if form.is_valid():
#             subiect = form.cleaned_data["subiect"]
#             mesaj = form.cleaned_data["mesaj"]
#             email = form.cleaned_data["email"]
#     return redirect("/")

def custom_login(request):
    form = CustomLoginForm()
    if request.method == "POST":
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            login(request, form.authenticated_user)
            return redirect("/")

    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect("/")