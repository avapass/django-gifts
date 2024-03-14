from django.shortcuts import render
from django.http import HttpResponse

from .models import Product

# Create your views here.

def products_list(request):
    products = Product.objects.all()
    products_fixed = [
        f"<li>{product.title} - {product.price}</li>"
        for product in products
    ]
    response_string = "<ol>"
    response_string += "".join(products_fixed)
    response_string += "</ol>"

    return HttpResponse(response_string)