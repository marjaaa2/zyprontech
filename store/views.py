from django.shortcuts import render, get_object_or_404
from .models import Product


def home(request):
    products = Product.objects.order_by('-created_at')[:6]
    return render(request, 'store/home.html', {'products': products})


def product_list(request):
    products = Product.objects.order_by('-created_at')
    return render(request, 'store/product_list.html', {'products': products})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'store/product_detail.html', {'product': product})