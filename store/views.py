from django.conf import settings
from django.http import JsonResponse, Http404
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import stripe

from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment, LiveEnvironment
from paypalcheckoutsdk.orders import OrdersCreateRequest, OrdersCaptureRequest

from .data import PRODUCTS

def home(request):
    products = PRODUCTS[:6]
    return render(request, 'store/home.html', {'products': products})


def product_list(request):
    return render(request, 'store/product_list.html', {'products': PRODUCTS})


def product_detail(request, slug):
    product = next((p for p in PRODUCTS if p["slug"] == slug), None)
    if not product:
        return render(request, 'store/product_not_found.html', status=404)

    return render(request, 'store/product_detail.html', {'product': product})