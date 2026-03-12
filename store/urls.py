from django.urls import path
from . import views

app_name = "store"

urlpatterns = [
    path("", views.home, name="home"),
    path("produse/", views.product_list, name="product_list"),
    path("produse/<slug:slug>/", views.product_detail, name="product_detail"),
]