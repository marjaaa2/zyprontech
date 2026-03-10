from django.conf import settings
from django.http import JsonResponse, Http404
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import stripe

from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment, LiveEnvironment
from paypalcheckoutsdk.orders import OrdersCreateRequest, OrdersCaptureRequest

from .data import PRODUCTS


def get_product_or_404(slug):
    product = next((p for p in PRODUCTS if p["slug"] == slug), None)
    if not product:
        raise Http404("Product not found")
    return product


def home(request):
    products = PRODUCTS[:6]
    return render(request, 'store/home.html', {'products': products})


def product_list(request):
    return render(request, 'store/product_list.html', {'products': PRODUCTS})


def product_detail(request, slug):
    product = get_product_or_404(slug)
    return render(
        request,
        'store/product_detail.html',
        {
            'product': product,
            'paypal_client_id': settings.PAYPAL_CLIENT_ID,
            'site_url': settings.SITE_URL,
        }
    )


def payment_success(request):
    return render(request, 'store/payment_success.html')


def payment_cancel(request):
    return render(request, 'store/payment_cancel.html')


@csrf_exempt
def create_stripe_checkout_session(request, slug):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    product = get_product_or_404(slug)
    stripe.api_key = settings.STRIPE_SECRET_KEY

    session = stripe.checkout.Session.create(
        mode="payment",
        line_items=[
            {
                "price_data": {
                    "currency": "ron",
                    "product_data": {
                        "name": product["name"],
                        "description": product["description"][:200],
                    },
                    "unit_amount": int(product["price_value"] * 100),
                },
                "quantity": 1,
            }
        ],
        success_url=f"{settings.SITE_URL}/payment/success/",
        cancel_url=f"{settings.SITE_URL}/payment/cancel/",
    )

    return JsonResponse({"url": session.url})


def get_paypal_client():
    if settings.PAYPAL_MODE == "live":
        environment = LiveEnvironment(
            client_id=settings.PAYPAL_CLIENT_ID,
            client_secret=settings.PAYPAL_CLIENT_SECRET,
        )
    else:
        environment = SandboxEnvironment(
            client_id=settings.PAYPAL_CLIENT_ID,
            client_secret=settings.PAYPAL_CLIENT_SECRET,
        )
    return PayPalHttpClient(environment)


@csrf_exempt
def create_paypal_order(request, slug):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    product = get_product_or_404(slug)
    client = get_paypal_client()

    paypal_request = OrdersCreateRequest()
    paypal_request.prefer("return=representation")
    paypal_request.request_body(
        {
            "intent": "CAPTURE",
            "purchase_units": [
                {
                    "description": product["name"],
                    "amount": {
                        "currency_code": "USD",
                        "value": f'{product["price_value"]:.2f}',
                    },
                }
            ],
            "application_context": {
                "return_url": f"{settings.SITE_URL}/payment/success/",
                "cancel_url": f"{settings.SITE_URL}/payment/cancel/",
            },
        }
    )

    response = client.execute(paypal_request)
    return JsonResponse({"id": response.result.id})


@csrf_exempt
def capture_paypal_order(request, order_id):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    client = get_paypal_client()
    capture_request = OrdersCaptureRequest(order_id)
    capture_request.request_body({})

    response = client.execute(capture_request)
    return JsonResponse(
        {
            "status": response.result.status,
            "id": response.result.id,
        }
    )