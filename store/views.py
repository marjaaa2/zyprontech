from django.http import Http404, JsonResponse
from django.shortcuts import render
from django.conf import settings
import requests

from .data import PRODUCTS


def get_product_or_404(slug):
    product = next((p for p in PRODUCTS if p["slug"] == slug), None)
    if not product:
        raise Http404("Product not found")
    return product


def home(request):
    products = PRODUCTS[:6]
    return render(request, "store/home.html", {"products": products})


def product_list(request):
    return render(request, "store/product_list.html", {"products": PRODUCTS})


def product_detail(request, slug):
    product = get_product_or_404(slug)
    return render(request, "store/product_detail.html", {"product": product})


def printful_stores(request):
    headers = {
        "Authorization": f"Bearer {settings.PRINTFUL_API_TOKEN}",
        "Content-Type": "application/json",
    }

    response = requests.get(
        "https://api.printful.com/v2/stores",
        headers=headers,
        timeout=30
    )

    return JsonResponse(response.json(), safe=False)