from django.shortcuts import render
from django.http import HttpResponse

from .models import Product

# Create your views here.

def hello(request):
    return render(request, "index.html")

def products_list(request):
    products = Product.objects.all()
    products = products.order_by("-price", "title")

    return render(request, "products.html", {"products": products})

def product(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return HttpResponse("404")
    return HttpResponse(f"{product}")